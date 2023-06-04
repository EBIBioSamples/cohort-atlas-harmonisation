import requests
import os


def test_labels(file_path: str):

    if not os.path.exists(file_path):
        print(f"This file doesn't exist: {file_path}")
        return dict()

    params = {
        'path': file_path
    }

    url = f"http://localhost:3000/match"

    response = requests.get(url, params)
    status_code = response.status_code

    if status_code == 200:
        outp_json = response.json()
        print(f"Response json is: {outp_json}")
    else:
        outp_json = dict()
        print(f"Request failed with status code: {status_code}; file path: {file_path}")

    return outp_json


if __name__ == '__main__':
    test_labels(file_path=f"/app/shared/sample_labels_to_annotate.csv")
