from flask import Flask, jsonify, request
import random
import logging
import sys

app = Flask(__name__)

# Simulated data for the microservices
microservices_data = {
    "Frog1": {"version": 1, "state": "healthy"},
    "Frog2": {"version": 1, "state": "healthy"},
    "Frog3": {"version": 1, "state": "healthy"},
    "Frog4": {"version": 1, "state": "healthy"},
    "Frog5": {"version": 1, "state": "healthy"},
}

# Initialize a logger
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("PondPulse")

@app.route('/')
def index():
    return "PondPulse Microservice"

@app.route('/microservices', methods=['GET'])
def get_microservices():
    return jsonify(microservices_data)

@app.route('/microservices/<microservice_name>', methods=['GET'])
def get_microservice(microservice_name):
    if microservice_name in microservices_data:
        return jsonify(microservices_data[microservice_name])
    else:
        return jsonify({"message": "Microservice not found"}), 404

@app.route('/microservices/<microservice_name>', methods=['PUT'])
def update_microservice(microservice_name):
    if microservice_name in microservices_data:
        try:
            data = request.get_json()
            new_state = data.get("state")
            if new_state in ["healthy", "insecure", "slow"]:
                microservices_data[microservice_name]["state"] = new_state
                logger.info(f"Updated state of {microservice_name} to {new_state}")
                return jsonify({"message": f"Updated state of {microservice_name} to {new_state}"}), 200
            else:
                return jsonify({"message": "Invalid state"}), 400
        except Exception as e:
            logger.error(f"Error updating state of {microservice_name}: {str(e)}")
            return jsonify({"message": "Error updating state"}), 500
    else:
        return jsonify({"message": "Microservice not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
