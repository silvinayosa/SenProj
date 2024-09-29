from flask import Flask, jsonify, request, abort
from flask_cors import CORS  # Import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define the path to your CSV files directory
CSV_DIR = '/Users/andersonbernardo/Documents/GitHub/SenProj/SenProj/Database/database-csv/co2-csv'

@app.route('/api/data/<city>', methods=['GET'])
def get_data(city):
    # Construct the file path for the specified city
    csv_file_path = os.path.join(CSV_DIR, f'{city}_avg_co2.csv')

    # Check if the file exists
    if not os.path.isfile(csv_file_path):
        abort(404)  # Return a 404 error if the file does not exist

    # Load the CSV file
    df = pd.read_csv(csv_file_path)

    # Get the last 6 rows and convert to a list of dictionaries
    last_six = df.tail(6).to_dict(orient='records')
    
    return jsonify(last_six)

if __name__ == '__main__':
    app.run(debug=True)
