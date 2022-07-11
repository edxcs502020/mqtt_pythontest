# Python application to subcribe to message broker

import paho.mqtt.client as mqtt
import time
from threading import Thread

def main():
    # Create lists for each thread
    global one_min
    one_min = []

    global five_min
    five_min = []
    
    global thirty_min
    thirty_min = []

    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect("localhost", 1883, 30)

    # Multithreading functions found at https://www.programiz.com/python-programming/time/sleep
    one_min_thread = Thread(target=calc_one_min_avg, args=(one_min, mqtt_client))
    five_min_thread = Thread(target=calc_five_min_avg, args=(five_min, mqtt_client))
    thirty_min_thread = Thread(target=calc_thirty_min_avg, args=(thirty_min,mqtt_client))

    # Begin averages calculations
    start_threads(one_min_thread, five_min_thread, thirty_min_thread)

    mqtt_client.loop_forever()

# on_connect, on_message and loop_forever() functions below were used from the Eclipse Paho 
# documentation found at https://www.eclipse.org/paho/index.php?page=clients/python/index.php

# Subscribe to created "rand_num" topic
def on_connect(client, userdata, flags, rc):
    client.subscribe("topic/rand_num")

# Get subscribed integers from broker
def on_message(client, userdata, message):
    value = int(message.payload)
    # Populate lists for average calculation
    one_min.append(value)
    five_min.append(value)
    thirty_min.append(value)

# Calculate time-based averages, each run as its own thread
def calc_one_min_avg(x, client):
    while True:
        time.sleep(60)
        one_min_avg = sum(x) / len(x)
        client.publish("topic/one_min_avg", one_min_avg)
        x.clear()


def calc_five_min_avg(y, client):
    while True:
        time.sleep(60*5)
        five_min_avg = sum(y) / len(y)
        client.publish("topic/five_min_avg", five_min_avg)
        y.clear()


def calc_thirty_min_avg(z, client):
    while True:
        time.sleep(60*30)
        thirty_min_avg = sum(z) / len(z)
        client.publish("topic/thirty_min_avg", thirty_min_avg)
        z.clear()


def start_threads(thread1, thread2, thread3):
    thread1.start()
    thread2.start()
    thread3.start()


if __name__ == "__main__":
    main()