from flask import Flask, jsonify, abort
from flask_cors import CORS  # Import CORS
import os
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define the path to your JSON files directory
JSON_DIR = '/Users/andersonbernardo/Documents/GitHub/SenProj/SenProj/Database/database-csv/cost-json'

@app.route('/api/data/<city>', methods=['GET'])
def get_data(city):
    # Construct the file path for the specified city
    json_file_path = os.path.join(JSON_DIR, f'{city}_price_ranges_with_percentage.json')

    # Check if the file exists
    if not os.path.isfile(json_file_path):
        abort(404)  # Return a 404 error if the file does not exist

    # Load the JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
