from flask import Flask, jsonify, json, Response, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def errorResponse():
    return jsonify({"message" : "Nothing here, used for health check. Try /mysfits instead."})

@app.route("/mysfits")
def getProducts():


    response = Response(open("mysfits-response.json").read())
    response.headers["Content-Type"]= "application/json"

    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
