import requests
import random
import time
import json
import logging
import sys

# PondPulse API URL
pondpulse_url = "http://pondpulse-service/microservices"
headers = {'Content-Type': 'application/json'}

# Initialize a logger
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("FlyTrap")

# Function to simulate monitoring of microservices
def monitor_microservices():
    while True:
        try:
            # Simulate monitoring of each microservice
            for microservice_name in ["Frog1", "Frog2", "Frog3", "Frog4", "Frog5"]:
                # Simulate performance and security checks (replace with your logic)
                is_slow = random.choice([True, False])
                is_insecure = random.choice([True, False])

                if is_slow or is_insecure:
                    # Notify PondPulse to modify the state of "healthy" apps
                    new_state = "slow" if is_slow else "insecure"
                    payload = {"state": new_state}
                    response = requests.put(f"{pondpulse_url}/{microservice_name}", data=json.dumps(payload), headers=headers)

                    if response.status_code == 200:
                        logger.info(f"Updated state of {microservice_name} to {new_state}")
                    else:
                        logger.error(f"Failed to update state of {microservice_name}")

            # Sleep for a random interval before checking again (adjust as needed)
            time.sleep(random.randint(30, 60))
        except Exception as e:
            logger.error(f"Error: {e}")

if __name__ == '__main__':
    monitor_microservices()
