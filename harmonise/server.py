import pandas as pd
from flask import Flask, render_template, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

from harmonise.annotator_tfidf import AnnotatorTfidf
from harmonise.app_config import SERVER_ADDRESS, SERVER_PORT

app = Flask(__name__)
cors = CORS(app)


@app.route("/")
def health():
    return {"status": "up"}


@app.route('/harmonise', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('harmonise.html')
    if request.method == 'POST':
        return harmonise_dictionary()


def harmonise_dictionary():
    if request.is_json:
        return harmonise_dictionary_json()
    else:
        return harmonise_dictionary_file()


def harmonise_dictionary_file():
    f = request.files['file']
    file_path = 'resources/uploads/' + secure_filename(f.filename)
    f.save(file_path)
    return read_file_and_convert_to_json(file_path)


def harmonise_dictionary_json():
    cohort = request.get_json()  # force=true?
    cohort_name = cohort['name']
    cohort_dictionary = cohort['dictionary']

    df = pd.DataFrame(cohort_dictionary)
    file_path = 'resources/uploads/' + secure_filename(cohort_name) + '.csv'
    df.to_csv(file_path, index=False)

    return read_file_and_convert_to_json(file_path)


def read_file_and_convert_to_json(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.lower()
    df = df.fillna("")

    annotated_df = annotate_with_labels(file_path)
    df["suggestions"] = annotated_df["CLASS"]

    annotations = df.to_dict(orient='records')
    for record in annotations:
        record["annotation"] = record["suggestions"]
        record["suggestions"] = [{"fieldName": record["suggestions"], "matchPercentage": 75}]

    return annotations


def annotate_with_labels(file_path):
    df = pd.read_csv(file_path)
    annotated_df = AnnotatorTfidf().annotate(df)
    print(annotated_df)
    return annotated_df


if __name__ == '__main__':
    app.run(host=SERVER_ADDRESS, port=SERVER_PORT, debug=False)
