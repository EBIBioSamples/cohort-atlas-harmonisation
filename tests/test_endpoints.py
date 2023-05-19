import requests
import os


def test_labels(file_path: str):
    url = f"http://localhost:5000//match/{file_path}"

    response = requests.get(url)
    status_code = response.status_code

    if status_code == 200:
        outp_json = response.json()
        print(f"Response json is: {outp_json}")
    else:
        print(f"Request failed with status code: {status_code}")


if __name__ == '__main__':
    current_dir = os.getcwd()
    test_labels(file_path=f"{current_dir}/sample_labels_to_annotate.csv")
