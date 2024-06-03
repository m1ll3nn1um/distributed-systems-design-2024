from flask import Flask, jsonify, request
import requests

messages = {}

app = Flask(__name__)
@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        msg="Not implemented yet"
        return msg
    else:
        return jsonify({'error': 'Bad request'})


if __name__ == '__main__':
    app.run(debug=True, port=5005)