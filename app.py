import os
from flask import Flask
from flask import render_template
from flask import jsonify, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from lib import search
secret_key = 'SomethingSecret'

UPLOAD_FOLDER = 'C:\\Users\\ediss\\Google Drive\\Inteligencia Artificial\\busquedasAIWeb\\uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template('index.html', title="Busquedas")

@app.route("/result")
def result():
    filename=request.args.get('filename')
    return render_template('result.html', title="Resultado de busquedas", filename=filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/buscar', methods=['POST'])
def buscar():
  inputFile = request.form['inputFile']
  print(inputFile)
  return redirect( url_for('result'))


@app.route('/file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'inputFile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['inputFile']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('result',
                                    filename=filename))