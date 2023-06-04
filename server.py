from flask_cors import CORS
import pandas as pd
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import socket
from dotenv import load_dotenv
import psutil

import harmonise.annotator
from harmonise.match import get_match


load_dotenv('./env')
FLASK_PORT = int(os.getenv('FLASK_PORT'))

app = Flask(__name__)
app.config['ENV'] = 'production'
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


@app.route('/match', methods=['GET'])
def field_match():
    path = request.args.get('path', type=str)

    if not os.path.exists(path):
        print(f"This file path is not exist: {path}")

    match_dict = get_match(file_path=path)
    return match_dict


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


def is_port_avaiable(port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    outp = sock.connect_ex(('localhost', port))
    sock.close()
    return outp != 0


def run_flask():
    global FLASK_PORT
    global app

    if is_port_avaiable(port=FLASK_PORT):
        app.run(host='0.0.0.0', port=FLASK_PORT, debug=False)
    else:
        print(f"Port {FLASK_PORT} is already in use. Please, release the port")
        for proc in psutil.process_iter(['pid', 'name']):
            connections = proc.connections()
            for conn in connections:
                if conn.status == psutil.CONN_LISTEN and conn.laddr.port == FLASK_PORT:
                    print(f"Process is: {proc}")
                    break


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    run_flask()
