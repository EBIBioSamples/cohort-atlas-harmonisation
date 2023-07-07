import requests
import os
from dotenv import load_dotenv
from itertools import islice
import pytest

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

    assert len(outp_json) > 0, "Empty json"
    assert len(outp_json) == 29, "Wrong size json"

    first_5_elements = dict(islice(outp_json.items(), 5))

    expected_values = {
        'Age at present': {'confidence': 'MEDIUM', 'propertyValue': 'mating_type_region',
                           'semanticTags': ['http://purl.obolibrary.org/obo/SO_0001789']},
        'Age at the agreement date': {'confidence': 'MEDIUM', 'propertyValue': 'mating_type_region',
                                      'semanticTags': ['http://purl.obolibrary.org/obo/SO_0001789']},
        'Agreement date': {'confidence': 'MEDIUM', 'propertyValue': 'mating_type_region',
                           'semanticTags': ['http://purl.obolibrary.org/obo/SO_0001789']},
        'Alcohol consumption habits': {'confidence': 'MEDIUM', 'propertyValue': 'mating_type_region',
                                       'semanticTags': ['http://purl.obolibrary.org/obo/SO_0001789']},
        'Birthdate': {'confidence': 'MEDIUM', 'propertyValue': 'mating_type_region',
                      'semanticTags': ['http://purl.obolibrary.org/obo/SO_0001789']}
    }

    for key, value in first_5_elements.items():
        assert key in expected_values, f"Unexpected key in json: {key}"
        assert value == expected_values[key], f"Unexpected value for key {key} in json. " \
                                              f"Expected: {expected_values[key]}. Got: {value}"

    return outp_json


if __name__ == '__main__':
    test_labels(file_path=f"sample_labels_to_annotate.csv")
