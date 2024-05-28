# task 5
import hazelcast
import time


def task5_1():
    client = hazelcast.HazelcastClient(cluster_name="ps_cluster", cluster_members=[])
    try:
        queue =  client.get_queue("ps_queue").blocking()
        for i in range(1, 101):
            queue.put(i)
            print(i)
            time.sleep(1)
    finally:
        client.shutdown()

task5_1()