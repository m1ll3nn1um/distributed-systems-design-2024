import hazelcast
import time

def task3():
    client = hazelcast.HazelcastClient(cluster_name="ps_cluster", cluster_members=[])
    try:
        map = client.get_map("distributed-map").blocking()
        map.put_all({i: i for i in range(1, 1001)})
    finally:
        client.shutdown()

task3()

