from flask import Flask, jsonify, json, Response, request
from flask_cors import CORS
import mysfitsTableClient

app = Flask(__name__)
CORS(app)

@app.route("/")
def errorResponse():
    return jsonify({"message" : "Nothing here, used for health check. Try /mysfits instead."})

@app.route("/mysfits")
def getMysfits():

    filterCategory = request.args.get('filter')
    if filterCategory:
        filterValue = request.args.get('value')
        queryParam = {
            'filter': filterCategory,
            'value': filterValue
        }
        serviceResponse = mysfitsTableClient.queryMysfits(queryParam)
    else:
        serviceResponse = mysfitsTableClient.getAllMysfits()

    flaskResponse = Response(serviceResponse)
    flaskResponse.headers["Content-Type"] = "application/json"

    return flaskResponse

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
