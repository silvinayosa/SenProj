from flask import Flask, request, jsonify
import sqlite3
import random
from datetime import datetime, timedelta
from flask_cors import CORS 
import bcrypt

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Connect to the database
def connect_to_db():
    conn = sqlite3.connect("SeniorProject.db", check_same_thread=False)
    return conn

def insert_user(data):
    first_name = data.get('FirstName')
    last_name = data.get('LastName')
    email = data.get('Email')
    password = data.get('Password')

    if not first_name or not last_name or not email or not password:
        return {"error": "Missing required fields"}, 400

    verification_code = random.randint(100000, 999999)
    token_expiry = datetime.now() + timedelta(minutes=10)  # 令牌10分鐘後過期
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user (FirstName, LastName, Email, Password, Verification_code, Token_Expiry)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, hashed_password, verification_code, token_expiry))
        conn.commit()
        return {"message": "User created successfully! Please check your email to verify your account"}, 201
    except sqlite3.IntegrityError:
        return {"error": "Email already exists"}, 400
    except sqlite3.Error as e:
        return {"error": str(e)}, 500
    finally:
        if conn:
            conn.close()

def get_user_by_email(email):
    conn = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute('SELECT ID, FirstName, LastName, Email, Verification_code, Verified, Token, Token_Expiry FROM user WHERE Email = ?', (email,))
        user = cursor.fetchone()
        if user:
            user_data = {
                "ID": user[0],
                "FirstName": user[1],
                "LastName": user[2],
                "Email": user[3],
                "Verification_code": user[4],
                "Verified": user[5],
                "Token": user[6],
                "Token_Expiry": user[7]
            }
            return user_data, 200
        else:
            return {"error": "User not found"}, 404
    except sqlite3.Error as e:
        return {"error": str(e)}, 500
    finally:
        if conn:
            conn.close()
def get_user_by_id(user_id):
    conn = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute('SELECT ID, FirstName, LastName, Email, Verification_code, Verified, Token, Token_Expiry FROM user WHERE ID = ?', (user_id,))
        user = cursor.fetchone()
        if user:
            user_data = {
                "ID": user[0],
                "FirstName": user[1],
                "LastName": user[2],
                "Email": user[3],
                "Verification_code": user[4],
                "Verified": user[5],
                "Token": user[6],
                "Token_Expiry": user[7]
            }
            return user_data, 200
        else:
            return {"error": "User not found"}, 404
    except sqlite3.Error as e:
        return {"error": str(e)}, 500
    finally:
        if conn:
            conn.close()

def update_user_by_email(email, data):
    conn = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        update_fields = []
        update_values = []
        
        if 'FirstName' in data:
            update_fields.append("FirstName = ?")
            update_values.append(data['FirstName'])
        if 'LastName' in data:
            update_fields.append("LastName = ?")
            update_values.append(data['LastName'])
        if 'Email' in data and data['Email'] != email:  
            update_fields.append("Email = ?")
            update_values.append(data['Email'])
        if 'Password' in data:
            hashed_password = bcrypt.hashpw(data['Password'].encode('utf-8'), bcrypt.gensalt())
            update_fields.append("Password = ?")
            update_values.append(hashed_password)

        if not update_fields:
            return {"error": "No fields provided to update"}, 400

        update_values.append(email)
        update_query = f"UPDATE user SET {', '.join(update_fields)} WHERE Email = ?"
        cursor.execute(update_query, update_values)
        conn.commit()

        if cursor.rowcount == 0:
            return {"error": "User not found"}, 404

        return {"message": "User update successful!"}, 200
    except sqlite3.Error as e:
        return {"error": str(e)}, 500
    finally:
        if conn:
            conn.close()

def delete_user_by_email(email):
    conn = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM user WHERE Email = ?', (email,))
        conn.commit()

        if cursor.rowcount == 0:
            return {"error": "User not found"}, 404

        return {"message": "User has been deleted successfully"}, 200
    except sqlite3.Error as e:
        return {"error": str(e)}, 500
    finally:
        if conn:
            conn.close()


# Create user
# http://127.0.0.1:5000/api/users/add
@app.route("/api/users/add", methods=['POST'])
def api_add_user():
    data = request.get_json()
    response, status_code = insert_user(data)
    return jsonify(response), status_code

# Get user information based on email
# http://127.0.0.1:5000/api/users/<email>
@app.route("/api/users/<email>", methods=['GET'])
def api_get_user(email):
    response, status_code = get_user_by_email(email)
    return jsonify(response), status_code

# Get user information based on id
# http://127.0.0.1:5000/api/users/id/<user_id>
@app.route("/api/users/id/<int:user_id>", methods=['GET'])
def api_get_user_by_id(user_id):
    response, status_code = get_user_by_id(user_id)
    return jsonify(response), status_code


# Update user information based on email
# http://127.0.0.1:5000/api/users/email/<email>
@app.route("/api/users/email/<string:email>", methods=['PUT'])
def api_update_user_by_email(email):
    data = request.get_json()
    response, status_code = update_user_by_email(email, data)
    return jsonify(response), status_code


# Delete users based on email
# http://127.0.0.1:5000/api/users/email/<email>
@app.route("/api/users/email/<string:email>", methods=['DELETE'])
def api_delete_user_by_email(email):
    response, status_code = delete_user_by_email(email)
    return jsonify(response), status_code



@app.route("/", methods=['GET'])
def home():
    return "Flask is running!"

if __name__ == '__main__':
    app.run(debug=True)
