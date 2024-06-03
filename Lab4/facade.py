from flask import Flask, request, jsonify
import random
import requests
import hazelcast

hz = hazelcast.HazelcastClient(cluster_name="ps_cluster", cluster_members=[])
messages_queue = hz.get_queue("queue").blocking()

def generate_unique_key():
   return ''.join(random.choices('123456789', k=4))

app = Flask(__name__)
@app.route('/data', methods=['GET', 'POST'])
def handle_data():
    logging_port = random.randint(5001, 5003)
    message_port = random.randint(5005, 5006)
    if request.method == 'GET':
        response_logging  = requests.get(f'http://127.0.0.1:{logging_port}/data', timeout=5)
        response_logging.raise_for_status()
        response_message = requests.get(f'http://127.0.0.1:{message_port}/data').text
        return jsonify({'Message data': response_message, 'Log data': response_logging.text})
    elif request.method == 'POST':
        message = request.get_data().decode('utf-8')
        messages_queue.offer(message)
        key=generate_unique_key()
        data = {"key": key, "msg": message}
        print(data)
        response = requests.post(f'http://127.0.0.1:{logging_port}/data', data=data)
        print("Response:", response.text)
        data = response.text
        return data

if __name__ == '__main__':
    app.run(debug=True,port=5000)