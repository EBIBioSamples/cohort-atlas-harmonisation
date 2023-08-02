import pandas as pd
from flask import Flask, render_template, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

import harmonise.annotator

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
    file_path = 'uploads/' + secure_filename(f.filename)
    f.save(file_path)
    return read_file_and_convert_to_json(file_path)


def harmonise_dictionary_json():
    cohort = request.get_json()  # force=true?
    cohort_name = cohort['name']
    cohort_dictionary = cohort['dictionary']

    df = pd.DataFrame(cohort_dictionary)
    file_path = 'uploads/' + secure_filename(cohort_name) + '.csv'
    df.to_csv(file_path, index=False)

    return read_file_and_convert_to_json(file_path)


# @app.route('/uploader', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files['file']
#         file_path = 'uploads/' + secure_filename(f.filename)
#         f.save(file_path)
#         return read_file_and_convert_to_json(file_path)
#
#
# @app.route('/uploader_json', methods=['POST'])
# def upload_file_json():
#     print(request.form)
#     print(request.is_json)
#     cohort = request.get_json()  # force=true?
#     cohort_name = cohort['name']
#     cohort_dictionary = cohort['dictionary']
#
#     df = pd.DataFrame(cohort_dictionary)
#     file_path = 'uploads/' + secure_filename(cohort_name) + '.csv'
#     df.to_csv(file_path, index=False)
#
#     return read_file_and_convert_to_json(file_path)


def read_file_and_convert_to_json(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.lower()
    df = df.fillna("")
    # result = df.to_json(orient="split")
    # parsed = loads(result)
    # json_dictionary = dumps(parsed, indent=4)
    # return json_dictionary

    annotated_df = annotate_with_labels(file_path)
    df["suggestions"] = annotated_df["CLASS"]

    annotations = df.to_dict(orient='records')
    for record in annotations:
        record["suggestions"] = [record["suggestions"]]

    return annotations


def annotate_with_labels(file_path):
    annotated_df = harmonise.annotator.get_annotated_dataframe(file_path)
    print(annotated_df)
    return annotated_df


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host='0.0.0.0', port=9000, debug=False)

    # df = pd.read_csv('uploads/' + 'sample_labels_to_annotate.csv')
    # print(df.to_dict(orient='records'))
    # # result = df.to_json(orient="split")
    # # parsed = loads(result)
    # # json_dictionary = dumps(parsed, indent=4)
    # # print(json_dictionary)
