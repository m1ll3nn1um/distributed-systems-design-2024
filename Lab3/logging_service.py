from flask import Flask, jsonify, request
import requests
import hazelcast

app = Flask(__name__)

hz = hazelcast.HazelcastClient(cluster_name="ps_cluster", cluster_members=[])
messages_map = hz.get_map("messages").blocking()

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == "POST":
        key = request.form['key']
        message = request.form['msg']
        messages_map.put(key, message)
        print("New writing data:", key, message)
        return ("Success!")
    elif request.method == "GET":
        keys = messages_map.key_set()
        messages = []
        for key in keys:
            message = messages_map.get(key)
            messages.append(message)
        return "\n".join(messages)
    
if __name__ == '__main__':
    app.run(port=5003)