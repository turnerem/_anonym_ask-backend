# export FLASK_APP=app.py
# flask run --host=0.0.0.0 --port=5000

from flask import Flask, request
import pymongo
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
# from flask_socketio import SocketIO, join_room
import json
from private_configs import MONGO_URI
from utils.utils import user_exists, validate_sesh_struc


app = Flask(__name__)
CORS(app, resources={r'/api/*': {'origins': '*'}})


set_uri = MONGO_URI

# app.config["MONGO_URI"] = "mongodb+srv://douglashellowell:" + \
#     db_password + "@cluster0-wvchx.mongodb.net/" + db_name
mongo = PyMongo(app, uri=set_uri)

# On root request
@app.route('/api', methods=['POST'])
# @cross_origin()
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
# @cross_origin()
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
    app.run(threaded=True, host='0.0.0.0', port=5000)