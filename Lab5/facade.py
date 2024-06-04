from flask import Flask, request, jsonify
import random
import requests
import hazelcast
from Consul import *


service_id = Register_service('facade-service', 5000)

hz_config = json.loads(Get_value('HZ_config'))
print("Hazelcast config: ", hz_config)

hz = hazelcast.HazelcastClient(cluster_name=hz_config['cluster_name'], cluster_members=[])
messages_queue = hz.get_queue(hz_config['queue_name']).blocking()



def generate_unique_key():
   return ''.join(random.choices('123456789', k=4))

app = Flask(__name__)

@app.route('/data', methods=['GET', 'POST'])
def handle_data():
    logging_ip = Get_port("logging-service")
    message_ip = Get_port("message-service")
    if request.method == 'GET':
        response_logging  = requests.get(logging_ip, timeout=5)
        response_logging.raise_for_status()
        response_message = requests.get(message_ip).text
        return jsonify({'Message data': response_message, 'Log data': response_logging.text})
    elif request.method == 'POST':
        message = request.get_data().decode('utf-8')
        messages_queue.offer(message)
        key=generate_unique_key()
        data = {"key": key, "msg": message}
        print(data)
        response = requests.post(logging_ip, data=data)
        print("Response:", response.text)
        data = response.text
        return data

if __name__ == '__main__':
    app.run(debug=True,port=5000)
    print("Current_ID:",service_id)
    input("Press Enter to exit...\n")
    Deregister_service(service_id)