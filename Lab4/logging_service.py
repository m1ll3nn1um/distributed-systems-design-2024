from flask import Flask, jsonify, request
import hazelcast
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--logport", type=int, required=True)
parser.add_argument("--hzport", type=int, required=True)
args = parser.parse_args()

port = args.hzport
command = f'''konsole -e zsh -c "docker run -it --name {port}-member 
            --network hazelcast-network --rm -e HZ_NETWORK_PUBLICADDRESS=192.168.1.113:{port} 
            -e HZ_CLUSTERNAME=ps_cluster -p {port}:5701 hazelcast/hazelcast:5.4.0"'''
subprocess.Popen(command, shell=True)

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
    app.run(port=args.logport)