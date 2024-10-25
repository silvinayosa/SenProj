# import necessary modules
from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def run_spea2_model(event_name, event_type, guests, start_date, end_date, province, budget):
    # Run your SPEA2 optimization model here with the provided data.
    print("Received data:")

    venues = [
        {
            "optimal_venue": "G Hall",
            "co2_emission": 120.5,
            "total_cost": 8500,
            "province": "Ontario"
        },
        {
            "optimal_venue": "Lakeside Pavilion",
            "co2_emission": 80.2,
            "total_cost": 6500,
            "province": "Ontario"
        },
        {
            "optimal_venue": "Sunset Gardens",
            "co2_emission": 140.3,
            "total_cost": 7800,
            "province": "Ontario"
        }
    ]

    return venues 


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/spea-2', methods=['POST'])
def spea2_model():
    data = request.get_json()

    # Extract form data
    event_name = data.get('event_name')
    event_type = data.get('event_type')
    guests = data.get('guests')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    province = data.get('province')
    budget = data.get('budget')

    # Run the SPEA2 model with the provided data
    try:
        result = run_spea2_model(event_name, event_type, guests, start_date, end_date, province, budget)

        # Send the result back to the front-end
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)



