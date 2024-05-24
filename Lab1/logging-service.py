from flask import Flask, jsonify, request
import requests

messages = {}

app = Flask(__name__)
@app.route('/data', methods=['GET', 'POST'])

def data():
    if request.method == 'GET':
        print("Current data in loggingsrv:",messages)
        return messages
    elif request.method == 'POST':
        # Обробка POST запиту
        key = request.form['key']
        message = request.form['msg']
        messages[key] = message
        print("New writing data:",key,message)
        return("Success!")
    else:
        return jsonify({'error': 'Bad request'})


if __name__ == '__main__':
    app.run(debug=True, port=5001)