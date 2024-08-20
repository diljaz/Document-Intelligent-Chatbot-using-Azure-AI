#flask is a python library to create APIs
from flask import Flask, request, jsonify # flask is a python library for creating APIs
from main import vector_store, query
app = Flask(__name__)
DB = None
@app.route('/api/upload', methods = ['POST']) #@app.route is a decorator, it will help us in creating an endpoint of /api and /upload
def upload():
    print(request.json)
    if 'file_name' not in request.json:
        return jsonify({'error':'file_name is necessary'}), 400
    file_name = request.json['file_name']
    db = vector_store(file_name)
    global DB
    DB = db

    return jsonify({'success': 'file uploaded successfully'}), 200 # 200: the status code for 'Success'
# I have used the 'POST' request method, instead of 'GET' because, we didn't get the parameter in query
@app.route('/api/query', methods = ['POST']) # https request methods in the client-server aspect.
def query_():
    if 'query' not in request.json:
        return jsonify({'error':'query is necessary'}), 400 # 400: the status code for 'Bad Request'
    question = request.json['query']
    result = query(question,DB)
    return jsonify({'question': question, 'response': result}), 200, {'Content-Type': 'application/json'}

