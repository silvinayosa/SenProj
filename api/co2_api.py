from flask import Flask, request, jsonify
import sqlite3
import random
from datetime import datetime, timedelta
from flask_cors import CORS 

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

#  Connect to the database
def connect_to_db():
    conn = sqlite3.connect("SeniorProject.db", check_same_thread=False)
    return conn


from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Connect to the database
def connect_to_db():
    conn = sqlite3.connect("SeniorProject.db", check_same_thread=False)
    return conn

# Get co2 based on id
def get_co2_by_id(id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM estimated_co2 WHERE ID=?", (id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "ID": row[0],
            "Latitude": row[1],
            "Longitude": row[2],
            "DateTime": row[3],
            "Co2Emission": row[4]
        }
    else:
        return {"error": "Record not found"}, 404

# Get co2 based on datetime
def get_co2_by_datetime(date_value):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM estimated_co2 WHERE DateTime LIKE ?", (f"{date_value}%",))
    rows = cursor.fetchall()
    conn.close()
    if rows:
        results = []
        for row in rows:
            results.append({
                "ID": row[0],
                "Latitude": row[1],
                "Longitude": row[2],
                "DateTime": row[3],
                "Co2Emission": row[4]
            })
        return results
    else:
        return {"error": "No records found"}, 404

# Get all co2
def get_all_co2():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM estimated_co2")
    rows = cursor.fetchall()
    conn.close()
    results = []
    for row in rows:
        results.append({
            "ID": row[0],
            "Latitude": row[1],
            "Longitude": row[2],
            "DateTime": row[3],
            "Co2Emission": row[4]
        })
    return results



# Get co2 based on id
# http://127.0.0.1:5000/api/co2/<int:id>
@app.route('/api/co2/<int:id>', methods=['GET'])
def api_get_co2_by_id(id):
    result = get_co2_by_id(id)
    return jsonify(result)

# Get co2 based on date
#  http://127.0.0.1:5000/api/co2/datetime?datetime=YYYY-MM-DD
@app.route('/api/co2/datetime', methods=['GET'])
def api_get_co2_by_datetime():
    date_value = request.args.get('datetime')
    result = get_co2_by_datetime(date_value)
    return jsonify(result)


# Get all co2 
# http://127.0.0.1:5000/api/co2
@app.route('/api/co2', methods=['GET'])
def api_get_all_co2():
    result = get_all_co2()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)


