import requests
import time
import urllib3

class ChromaDBClient:
    def __init__(self, host='localhost', port=8000, retries=3, retry_delay=5):
        self.base_url = f'http://{host}:{port}'
        self.session = requests.Session()
        self.retries = retries
        self.retry_delay = retry_delay
        self._connect()

    def _connect(self):
        for attempt in range(self.retries):
            try:
                # Attempt to connect or perform a simple GET request to check connectivity
                response = self.session.get(f'{self.base_url}/api/v1/tenants/default_tenant')
                response.raise_for_status()  # Raise an error for bad responses
                print("Connected to ChromaDB server successfully.")
                break  # Exit the loop if connection is successful
            except (urllib3.exceptions.NewConnectionError, requests.exceptions.ConnectionError) as e:
                print(f"Attempt {attempt + 1} failed: Could not connect to the ChromaDB server. Are you sure it is running?")
                if attempt < self.retries - 1:
                    print(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    raise ValueError("Could not connect to a Chroma server. Are you sure it is running?") from e

# Example usage
try:
    client = ChromaDBClient()
except ValueError as e:
    print(e)