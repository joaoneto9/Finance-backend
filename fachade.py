from flask import Flask, jsonify, request
from services.user_repository import User_repository

user_enpoint = "/user"

# starting the connection with the data-base
user_repository = User_repository()

app = Flask(__name__)

@app.get(user_enpoint)
def get_user():
    return jsonify(), 200

@app.post(user_enpoint)
def register_user():
    data = request.get_json()
    
    if not user_repository.register_user(data['username'], data['email'], data['password']):
        return jsonify({"reponse": "usuário ja tem cadastro, realize o login."}), 400
    
    return jsonify({"reponse": "usuário cadastrado com sucesso."}), 200

@app.post(user_enpoint + "/login")
def login_user():
    return jsonify(), 200