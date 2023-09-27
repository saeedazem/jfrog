import requests
import sqlite3
import time
import logging
import sys

# PondPulse API URL
pondpulse_url = "http://pondpulse-service/microservices"

# Initialize a logger
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("Dbribbit")

# Function to create a SQLite database and table if they don't exist
def create_database():
    conn = sqlite3.connect('dbribbit.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faulty_versions (
            id INTEGER PRIMARY KEY,
            microservice_name TEXT,
            version INTEGER,
            state TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    logging.info("Created Table faulty_versions in DB dbribbit.db")

# Function to periodically poll PondPulse and persist faulty versions to the database
def poll_and_persist():
    while True:
        try:
            response = requests.get(pondpulse_url)
            data = response.json()

            for microservice_name, info in data.items():
                if info['state'] in ["insecure", "slow"]:
                    # Persist faulty version to the database
                    conn = sqlite3.connect('dbribbit.db')
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO faulty_versions (microservice_name, version, state)
                        VALUES (?, ?, ?)
                    ''', (microservice_name, info['version'], info['state']))
                    conn.commit()
                    # can be used for validation and testing
                    # cursor.execute("SELECT * FROM faulty_versions")
                    # print(cursor.fetchall())
                    conn.close()
                    logging.info(f"Insert into table faulty_versions in dbribbit.db (microservice_name, version, state) with Values: ({microservice_name}, {info['version']}, {info['state']})")

            # Sleep for a specific interval before polling again (adjust as needed)
            time.sleep(300)  # Poll every 5 minutes
        except Exception as e:
            logging.error(f"Error: {e}")

if __name__ == '__main__':
    create_database()
    poll_and_persist()
