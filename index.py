from flask import Flask
from flask import render_template
from flask import jsonify, request, redirect, url_for

app = Flask(__name__)

from lib import search

@app.route("/")
def index():
    return render_template('index.html', title="Busquedas")

@app.route("/result")
def result():
    return render_template('result.html', title="Resultado de busquedas")

@app.route('/buscar', methods=['POST'])
def buscar():
  inputFile = request.form['inputFile']
  print(inputFile)
  return redirect( url_for('result'))