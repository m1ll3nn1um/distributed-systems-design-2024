from flask import Flask, jsonify, request
import hazelcast
import argparse
import subprocess
from Consul import *

parser = argparse.ArgumentParser()
parser.add_argument("--logport", type=int, required=True)
parser.add_argument("--hzport", type=int, required=True)
args = parser.parse_args()

service_id = Register_service('logging-service', args.logport)

command = f'konsole -e zsh -c "docker run -it --name {args.hzport}-member --network hazelcast-network --rm -e HZ_NETWORK_PUBLICADDRESS=192.168.1.113:{args.hzport} -e HZ_CLUSTERNAME=ps_cluster -p {args.hzport}:5701 hazelcast/hazelcast:5.4.0"'
subprocess.Popen(command, shell=True)

hz_config = json.loads(Get_value('HZ_config'))
print("Hazelcast config: ", hz_config)

hz = hazelcast.HazelcastClient(cluster_name=hz_config['cluster_name'], cluster_members=[])
messages_map = hz.get_map(hz_config['map_name']).blocking()

app = Flask(__name__)
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
    print("Current_ID:",service_id)
    input("Press Enter to exit...\n")
    Deregister_service(service_id)