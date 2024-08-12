from flask import Flask, request, jsonify
import sqlite3
import random
from datetime import datetime, timedelta
from flask_cors import CORS 


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Connect to the database
def connect_to_db():
    conn = sqlite3.connect("SeniorProject.db", check_same_thread=False)
    return conn

# get all venues
def get_all_venues():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM venue")
    venues = cursor.fetchall()
    conn.close()
    
    venue_list = []
    for venue in venues:
        venue_list.append({
            "ID": venue[0],
            "Facility_Name": venue[1],
            "ODRSF_facility_type": venue[2],
            "Prov_Terr": venue[3],
            "Latitude": venue[4],
            "Longitude": venue[5]
        })
    
    return venue_list

# get venues by type
def get_venues_by_type(facility_type):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM venue WHERE ODRSF_facility_type = ?", (facility_type,))
    venues = cursor.fetchall()
    conn.close()
    
    venue_list = []
    for venue in venues:
        venue_list.append({
            "ID": venue[0],
            "Facility_Name": venue[1],
            "ODRSF_facility_type": venue[2],
            "Prov_Terr": venue[3],
            "Latitude": venue[4],
            "Longitude": venue[5]
        })
    
    return venue_list

# get venues by prov_terr
def get_venues_by_prov(prov_terr):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM venue WHERE Prov_Terr = ?", (prov_terr,))
    venues = cursor.fetchall()
    conn.close()
    
    venue_list = []
    for venue in venues:
        venue_list.append({
            "ID": venue[0],
            "Facility_Name": venue[1],
            "ODRSF_facility_type": venue[2],
            "Prov_Terr": venue[3],
            "Latitude": venue[4],
            "Longitude": venue[5]
        })
    
    return venue_list

# get all venues 
# http://127.0.0.1:5000/venues

# get venues by type
# http://127.0.0.1:5000/venues?type=

# get venues by prov_terr
# http://127.0.0.1:5000/venues?prov=

@app.route('/venues', methods=['GET'])
def venues():
    facility_type = request.args.get('type')
    prov_terr = request.args.get('prov')

    if facility_type:
        venue_list = get_venues_by_type(facility_type)
    elif prov_terr:
        venue_list = get_venues_by_prov(prov_terr)
    else:
        venue_list = get_all_venues()

    if not venue_list:
        return jsonify({"error": "Not Found"}), 404

    return jsonify(venue_list)

if __name__ == '__main__':
    app.run(debug=True)