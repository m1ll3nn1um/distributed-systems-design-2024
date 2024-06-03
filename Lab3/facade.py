from flask import Flask, request, jsonify
import random
import requests

def generate_unique_key():
   return ''.join(random.choices('123456789', k=4))

app = Flask(__name__)
@app.route('/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'GET':
        port = random.randint(5001, 5003)
        response_logging  = requests.get(f'http://127.0.0.1:{port}/data', timeout=5)
        response_logging.raise_for_status()
        response_message = requests.get(f'http://127.0.0.1:5005/data').text
        return jsonify({'Message data': response_message  , 'Log data': response_logging.text})
    elif request.method == 'POST':
        message = request.get_data().decode('utf-8')
        key=generate_unique_key()
        port = random.randint(5001, 5003)
        data = {"key": key, "msg": message}
        print(data)
        response = requests.post(f'http://127.0.0.1:{port}/data', data=data)
        print("Response:", response.text)
        data = response.text
        return data

if __name__ == '__main__':
    app.run(debug=True,port=5000)