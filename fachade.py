from tkinter.tix import Tree
from flask import Flask, jsonify

user_enpoint = "/user"

app = Flask(__name__)

@app.get(user_enpoint)
def get_user():
    return jsonify(), 200

@app.post(user_enpoint)
def save_user():
    return jsonify(), 200

@app.post(user_enpoint + "/login")
def login_user():
    return jsonify(), 200