from doctest import debug
import email
from os import access
from pickle import TRUE
from flask import Flask, config, jsonify, request
from services.user_repository import User_repository
from flask_jwt_extended import JWTManager, create_access_token
import secrets

user_enpoint = "/user"

# starting the connection with the data-base
user_repository = User_repository()

app = Flask(__name__)

app.config.update(
    TESTING=True,
    SECRET_KEY=secrets.token_hex(16)
)  

jwt = JWTManager(app)
   
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
    data = request.get_json()
    
    try:
        user = user_repository.login_user(data['email'], data['password'])
        
        access_token = create_access_token(identity=data['email']) # type: ignore
        
        return jsonify({
            "username": user["username"], # type: ignore
            "token": access_token
        }), 200
    except Exception as e:
        return jsonify({"response": "usuário informou credencias incorretas"}), 400
