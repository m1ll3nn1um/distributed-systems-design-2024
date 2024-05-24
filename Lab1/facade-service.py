from flask import Flask, request, jsonify
import random
import requests

def generate_unique_key():
   return ''.join(random.choices('0123456789', k=4))

app = Flask(__name__)
@app.route('/data', methods=['GET', 'POST'])

def handle_data():
    if request.method == 'GET':
        # Обробка GET запиту
        response1 = requests.get(f'http://127.0.0.1:5001/data').text
        response2 = requests.get(f'http://127.0.0.1:5002/data').text
        return jsonify({'Message data': response1, 'Log data': response2})
    elif request.method == 'POST':
        message = request.get_data().decode('utf-8')
        key=generate_unique_key()
        data = {"key": key, "msg": message}
        print(data)
        response = requests.post(f'http://127.0.0.1:5001/data', data=data)
        print("Response", response.text)
        data = response.text
        return data

if __name__ == '__main__':
    app.run(debug=True)