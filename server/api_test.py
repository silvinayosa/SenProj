from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/process-data', methods=['GET'])
def process_data():
    response = {
        "dates": ["2023-05-01", "2023-05-02", "2023-05-03", "2023-05-04", "2023-05-05"],
        "actual_co2": [400, 410, 415, 420, 430],
        "rnn_predictions": [395, 405, 410, 415, 425],
        "lstm_predictions": [398, 408, 413, 418, 428]
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
