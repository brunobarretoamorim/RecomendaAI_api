from flask import Flask, request, render_template, jsonify

import json
from werkzeug.exceptions import HTTPException, BadRequest

from carregar_modelo import main

#app = Flask("Modelo")
app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')
  
@app.route("/doc")
def doc():
  return render_template('doc.html')

@app.route("/modelo", methods=["POST"])
def resultadoModelo():
    #carregar em lista o body da request
    body = request.get_json()
    materia = body['materia']
    respostas = body['data']


    resultado = main(materia, respostas)

    return jsonify(resultado)
    #return body
    
@app.route("/hello", methods=["GET"])
def test():
    return "Hello check!!!"

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return 'bad request!', 400

#app.run()
#app.run(host="0.0.0.0")