# export FLASK_APP=app.py
# flask run --host=0.0.0.0 --port=5000

from flask import Flask, request, jsonify
import pymongo
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import json
from private_configs import MONGO_URI
import eventlet



app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')


set_uri = MONGO_URI

# app.config["MONGO_URI"] = "mongodb+srv://douglashellowell:" + \
#     db_password + "@cluster0-wvchx.mongodb.net/" + db_name
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

# On root request
@app.route('/api', methods=['POST'])
def add_new_user():

    new_user = json.loads(request.data)
    # does username already exist?
    names = mongo.db.list_collection_names()
    userAlreadyExists = names.count(new_user['user_name']) > 0
    # {username: 'humanoid_gregory'}
    # print(new_user)
    # print('attemting to add "sessions" list')
    if (userAlreadyExists):
        return jsonify({"status": 409, "msg": "Please provide unique username"})
    else:
        new_user['sessions'] = []
        target_collection = mongo.db[new_user['user_name']]
        result = target_collection.insert_one(new_user)
        return jsonify({"status": 201, "insert_id": str(result.inserted_id)})


@app.route('/api/<user_name>', methods=['GET', 'POST'])
def add_session(user_name):
    # print('we get request')
    if(request.method == 'GET'):
        print('targetting collection')
        target_collection = mongo.db[user_name]
        print('targetted collection', target_collection)

        cursor_obj = target_collection.find({}, {'_id': 0})
        # cursor_obj = target_collection.find()
        print('the cursor object:', cursor_obj, dir(cursor_obj))

        
        result = []
        for x in cursor_obj:
            print('in loop?')
            result.append(x)
        print('\n\n\n\n\nthe result', result)
        return jsonify(result[0] if len(result) > 0 else {})

    elif(request.method == 'POST'):
        new_session = json.loads(request.data)
        target_collection = mongo.db[user_name]
        result = target_collection.update_one(
            {"user_name": user_name},
            {"$push": {'sessions': new_session}}
        )
        if (result.modified_count == 1):
            return jsonify({"status": 200})
        else:
            return jsonify({"status": 400})


@app.route('/api/<user_name>', methods=['DELETE'])
def delete_account(user_name):
    names = mongo.db.collection_names()
    userAlreadyExists = names.count(user_name) > 0
    if (userAlreadyExists):
        del_collection = mongo.db[user_name].drop()
        return jsonify({"status": 204})
    else:
        return jsonify({"status": 404})


@app.route('/api/<user_name>/<session_name>', methods=['GET', 'PATCH'])
def get_session(user_name, session_name):
    print('session name', session_name, user_name)
    if (request.method == 'GET'):
        target_collection = mongo.db[user_name]
        cursor_obj = target_collection.find(
            {'sessions.session_name': session_name},
            {'_id': 0, 'sessions.$': 1}
        )
        result = []
        for x in cursor_obj:
            result.append(x)
        print('\n\nA session?', result)
        return jsonify(result[0])
    elif (request.method == 'PATCH'):
        new_session = json.loads(request.data)
        target_collection = mongo.db[user_name]
        result = target_collection.update_one(
            {"user_name": user_name, "sessions.session_name": session_name},
            {"$set": {"sessions.$": new_session}}
        )
        return jsonify({"Did work? ": result.modified_count})

# @app.route('/api/<user_name>/<session_name>', methods=['DELETE'])
# def delete_session(user_name, session_name):


# @app.route('/api/<user_name>/<session_name>/<question_id>', methods=['PATCH'])
# def update_question(user_name, session_name, question_id):
#         new_answers = json.loads(request.data)
#         target_collection = mongo.db[user_name]
#         result = target_collection.update_one(
#             {
#                 "user_name": user_name,
#                 "sessions.session_name": session_name,
#                 "sessions.questions": question_id
#             },
#             {"$set": {"sessions.$.questions": new_answers}}
#         )
#         return jsonify({"Did work? ": result.modified_count})


if __name__ == '__main__':
    # threaded option to enable muptiple instances for multiple user access support (?!?!)
    app.debug = True
    # app.run(threaded=True, host='0.0.0.0', port=5000)
    socketio.run(app, host='0.0.0.0', port=5000)
