# task 4
import time
import hazelcast

def task2():
    client = hazelcast.HazelcastClient(cluster_name="ps_cluster", cluster_members=[])
    try:
        topic = client.get_topic("my-distributed-topic")
        listener = topic.add_listener(lambda message: print("Received:", message))
        time.sleep(20)
    finally:
        client.shutdown()

task2()
print("Pause 10sec")
time.sleep(10)
task2()