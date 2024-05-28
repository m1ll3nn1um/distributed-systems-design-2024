# task 4
import hazelcast
import time


def task1():
    client = hazelcast.HazelcastClient(cluster_name="ps_cluster", cluster_members=[])
    try:
        topic = client.get_topic("my-distributed-topic")
        for i in range(1, 101):
            topic.publish(i)
            print("Sent:", i)
            time.sleep(1)
    finally:
        client.shutdown()

task1()