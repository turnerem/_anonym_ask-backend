# export FLASK_APP=app.py
# flask run --host=0.0.0.0 --port=5000

from flask import Flask, request, jsonify
import pymongo
from flask_pymongo import PyMongo
import json

app = Flask(__name__)

db_password = 'dancingb'
db_name = 'meetings'

app.config["MONGO_URI"] = "mongodb+srv://douglashellowell:" + \
    db_password + "@cluster0-wvchx.mongodb.net/" + db_name
mongo = PyMongo(app)

# @app.route('/api', methods=['GET'])
# def get_collection_names():
#     # does username already exist?
#     names = mongo.db.list_collection_names()
#     return jsonify({"status": 201, "data": names})


# if __name__ == '__main__':
#     # threaded option to enable muptiple instances for multiple user access support (?!?!)
#     app.run(host='0.0.0.0', port=5000)



@app.route('/')
def say_fuck_off():
    return '\n\n\nfuck off\n^\_("/)_/^\n\n'
    # return jsonify({"msg": '\n\n\nfuck off\n\n\n'})


if __name__ == '__main__':
    # threaded option to enable muptiple instances for multiple user access support (?!?!)
    app.debug = True
    app.run(host='0.0.0.0', port=5000)