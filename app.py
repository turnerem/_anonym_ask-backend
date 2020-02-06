# export FLASK_APP=app.py
# flask run --host=0.0.0.0 --port=5000

from flask import Flask, request
import pymongo
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import json
from private_configs import MONGO_URI
import eventlet

from utils.utils import user_exists, validate_sesh_struc


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')


set_uri = MONGO_URI
mongo = PyMongo(app, uri=set_uri )


@socketio.on('presenter prompt')
def prompt_question(data, methods=['GET', 'POST']):
    print('\n')
    print(data)
    print('\n')
    print('sending to audience')
    socketio.emit('incoming question', data)


@socketio.on('end prompt')
def end_prompt(data, methods=['GET', 'POST']):
    print('\n')
    print('end prompt signal sent! \n')
    socketio.emit('end question')

@socketio.on('answer given')
def send_answer(data, methods=['GET', 'POST']):
    print('\nanswer sent!\n')
    socketio.emit('answer to presenter', data)

@socketio.on('text given')
def send_text_answer(data, method=['GET', 'POST']):
    print('\ntext answer sent!\n')
    print(str(data))
    socketio.emit('text to presenter', data)

# On root request
@app.route('/api', methods=['POST'])
def add_new_user():
    new_user = json.loads(request.data)
    if user_exists(mongo.db, new_user['user_name']):
        return {"msg": "Please provide unique username"}, 409
    else:
        new_user['sessions'] = []
        target_collection = mongo.db[new_user['user_name']]
        result = target_collection.insert_one(new_user)
        return {"insert_id": str(result.inserted_id)}, 201


@app.route('/api/<user_name>', methods=['GET'])
def get_sessions(user_name):
    target_collection = mongo.db[user_name]
    cursor_obj = target_collection.find({}, {'_id': 0})
    result = []
    for x in cursor_obj:
        result.append(x)
    if (len(result) > 0):
        return result[0], 200
    else: 
        return {'msg': 'User Not Found'}, 404


@app.route('/api/<user_name>', methods=['DELETE'])
def delete_account(user_name):
    if (user_exists(mongo.db, user_name)):
        del_collection = mongo.db[user_name].drop()
        return {'user_name': user_name}, 204
    else:
      return {'msg': 'User Not Found'}, 404


@app.route('/api/<user_name>', methods=['POST'])
def add_session(user_name):
    new_session = json.loads(request.data)
    # ensure new session is in correct format
    
    if not validate_sesh_struc(new_session):
        return {'msg': 'Bad Request'}, 400

    if not user_exists(mongo.db, user_name):
        return {"msg": "User Not Found"}, 409

    target_collection = mongo.db[user_name]
    result = target_collection.update_one(
        {"user_name": user_name},
        {"$push": {'sessions': new_session}}
    )
    if (result.modified_count == 1):
        return {'sessions': new_session}, 200



@app.route('/api/<user_name>/<session_name>', methods=['GET'])
# @cross_origin()
def get_session(user_name, session_name):
    target_collection = mongo.db[user_name]
    cursor_obj = target_collection.find(
        {'sessions.session_name': session_name},
        {'_id': 0, 'sessions.$': 1}
    )
    result = []
    for x in cursor_obj:
        result.append(x)
    if len(result) > 0:
        # print('\n\nget a single sesh', result[0]['sessions'][0])
        return result[0]['sessions'][0], 200
    elif not user_exists(mongo.db, user_name):
        return {'msg': 'User Not Found'}, 404
    else:
        return {'msg': 'Session Not Found'}, 404


@app.route('/api/<user_name>/<session_name>', methods=['PATCH'])
# @cross_origin()
def patch_session(user_name, session_name):
    updated_session = json.loads(request.data)
    if not validate_sesh_struc(updated_session):
        return {'msg': 'Bad Request'}, 400

    target_collection = mongo.db[user_name]
    result = target_collection.update_one(
        {"user_name": user_name, "sessions.session_name": session_name},
        {"$set": {"sessions.$": updated_session}}
    )
    return {}, 200


@app.route('/api/<user_name>/<session_name>', methods=['DELETE'])
def delete_session(user_name, session_name):
    target_collection = mongo.db[user_name]
    result = target_collection.delete_one(
        {"user_name": user_name, "sessions.session_name": session_name}
    )
    if result.deleted_count == 1:
      return {'session_name': session_name}, 204
    else: 
        return {'msg': 'Not Found'}, 404


if __name__ == '__main__':
    # threaded option to enable muptiple instances for multiple user access support (?!?!)
    app.debug = True
    app.run(threaded=True)
    # socketio.run(app, host='0.0.0.0', port=5000)
