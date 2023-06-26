import requests
import os
from dotenv import load_dotenv

load_dotenv('./env')
FLASK_PORT = int(os.getenv('FLASK_PORT'))


def test_labels(file_path: str):
    global FLASK_PORT

    if not os.path.exists(file_path):
        print(f"This file doesn't exist: {file_path}")
        return dict()

    url = f"http://localhost:{FLASK_PORT}/match"
    response = requests.post(url, files={'file': open(file_path, 'rb')})

    if response.status_code == 200:
        outp_json = response.json()
        print(f"Response json is: {outp_json}")
    else:
        outp_json = dict()
        print(f"Request failed with status code: {response.status_code}; file path: {file_path}")

    return outp_json


if __name__ == '__main__':
    test_labels(file_path=f"sample_labels_to_annotate.csv")
