from calendar import month
import os
from flask import Flask, jsonify, request
import psycopg
from services.user_repository import User_repository
from services.expense_repository import Expense_repository
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from datetime import datetime
import secrets
from flask_cors import CORS

user_enpoint = "/user"
expense_endpoint = "/expense"

# starting the connection with the data-base
conn: psycopg.Connection = psycopg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_FINANCE_DATABASE_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_USER_PASSWORD")
        )

user_repository = User_repository(conn=conn)
expense_repository = Expense_repository(conn=conn)

app = Flask(__name__)
CORS(app)

app.config.update(
    TESTING=True,
    SECRET_KEY=secrets.token_hex(16)
)  

jwt = JWTManager(app)
   
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
    

@app.post(expense_endpoint)
@jwt_required()
def register_expense():
    data = request.get_json()
    
    save_expense = expense_repository.register_expense(
                            datetime.today().strftime('%Y-%m-%d'), 
                            data['payment_date'], 
                            data['amount'], 
                            data['payment_description'], 
                            data['type_of_payment'],
                            get_jwt_identity())
    if not save_expense:
        return jsonify({"reponse": "erro ao cadatsrar um gasto, concerte os dados passados."}), 400
    
    return jsonify({"response": "gasto cadastrado com sucesso"}), 200

@app.get(expense_endpoint)
@jwt_required()
def get_users_expenses():

    date = request.args.get('date') # requiriment param for the date.
    is_specified_data = request.args.get("specified", "true").lower() # requiriment param to indicate teh specified query
    
    if date is not None:
        expenses = expense_repository.get_users_expenses_by_date(get_jwt_identity(), date, is_specified_data == "true")
    else:
        expenses = expense_repository.get_users_expenses(get_jwt_identity())

    return jsonify(expenses), 200

