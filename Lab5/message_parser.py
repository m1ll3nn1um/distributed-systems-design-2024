from flask import Flask, jsonify, request
import hazelcast
import argparse
import hazelcast
import threading
from Consul import *


parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, required=True)
args = parser.parse_args()

service_id = Register_service('message-service', args.port)


hz_config = json.loads(Get_value('HZ_config'))
print("Hazelcast config: ", hz_config)

hz = hazelcast.HazelcastClient(cluster_name=hz_config['cluster_name'], cluster_members=[])
messages_queue = hz.get_queue(hz_config['queue_name']).blocking()


app = Flask(__name__)
message_list=[]
def queue_event():
    while True:
        item = messages_queue.take()
        message_list.append(item)
        print("Recieved: ", str(item))

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        return '\n'.join(message_list)
    else:
        return jsonify({'error': 'Bad request'})


if __name__ == '__main__':
    event_thread = threading.Thread(target=queue_event)
    event_thread.start()
    app.run(port=args.port)
    print("Current_ID:", service_id)
    input("Press Enter to exit...\n")
    Deregister_service(service_id)