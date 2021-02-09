"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from twilio.rest import Client
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import Queue
from dotenv import load_dotenv
load_dotenv
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


user = Queue()
# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/new', methods=['POST'])
def handle_post():
    if not  request.json.get('name'):
        return jsonify({"name": "is required"}), 422
    if not  request.json.get('phone'):
        return jsonify({"phone": "is required"}), 422

    item = {
        "name": request.json.get('name'),
        "phone": request.json.get('phone')
    }
    msg = user.enqueue(item)
    return jsonify({"msg": "ok"}), 200

@app.route('/next', methods=['GET'])
def handle_get():
        item =user.dequeue()
        return jsonify({'msg': "Process next in row", "item": item}), 200

@app.route('/all', methods=['GET'])
def handle_get_all():
    fila = user.get_queue()
    return  jsonify(fila), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
