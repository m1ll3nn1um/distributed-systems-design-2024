from flask import Flask, jsonify, request
import hazelcast
import argparse
import hazelcast
import threading

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, required=True)
args = parser.parse_args()

hz  = hazelcast.HazelcastClient(cluster_name="ps_cluster", cluster_members=[])
messages_queue = hz.get_queue("queue").blocking()

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
    app.run(debug=True, port=args.port)