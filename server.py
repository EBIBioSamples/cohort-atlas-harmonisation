from flask_cors import CORS, cross_origin
import pandas as pd
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from json import loads, dumps

import harmonise.annotator

app = Flask(__name__)
cors = CORS(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        file_path = 'uploads/' + secure_filename(f.filename)
        f.save(file_path)
        return read_file_and_convert_to_json(file_path)


def read_file_and_convert_to_json(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.lower()
    df = df.fillna("")
    # result = df.to_json(orient="split")
    # parsed = loads(result)
    # json_dictionary = dumps(parsed, indent=4)
    # return json_dictionary

    annotated_df = annotate_with_labels(file_path)
    df["annotations"] = annotated_df["CLASS"]

    annotations = df.to_dict(orient='records')
    for record in annotations:
        record["annotations"] = [record["annotations"]]

    return annotations


def annotate_with_labels(file_path):
    annotated_df = harmonise.annotator.get_annotated_dataframe(file_path)
    print(annotated_df)
    return annotated_df


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()

    # df = pd.read_csv('uploads/' + 'sample_labels_to_annotate.csv')
    # print(df.to_dict(orient='records'))
    # # result = df.to_json(orient="split")
    # # parsed = loads(result)
    # # json_dictionary = dumps(parsed, indent=4)
    # # print(json_dictionary)
