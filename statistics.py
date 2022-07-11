# Python application to subcribe to message broker

import os
import paho.mqtt.client as mqtt
import time
from prettytable import PrettyTable
from threading import Thread

def main():
    # Using lists instead of temporary variables to retain useful time period data
    global one_min_stats
    one_min_stats = []

    global five_min_stats
    five_min_stats = []

    global thirty_min_stats
    thirty_min_stats = []


    # Create table structure, docs at https://pypi.org/project/prettytable/
    table = PrettyTable(['Time (mins)', 'One Minute Average', 'Five Minute Average', 'Thirty Minute Average'])

    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect("localhost", 1883, 30)

    # Begin draw_table thread
    table_thread = Thread(target=draw_table, args=(one_min_stats, five_min_stats, thirty_min_stats, table))
    table_thread.start()

    mqtt_client.loop_forever()

# on_connect, on_message and loop_forever() functions below were used from the Eclipse Paho 
# documentation found at https://www.eclipse.org/paho/index.php?page=clients/python/index.php

# Subscribe to created "avg" topics
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("topic/one_min_avg")
    client.subscribe("topic/five_min_avg")
    client.subscribe("topic/thirty_min_avg")

# Add subscribed averages to lists for display
def on_message(client, userdata, message):
    topic = str(message.topic)

    # Populate lists based on received topic
    if topic == "topic/one_min_avg":
        one_min_stats.append(float(message.payload))
    if topic == "topic/five_min_avg":
        five_min_stats.append(float(message.payload))
    if topic == "topic/thirty_min_avg":
        thirty_min_stats.append(float(message.payload))

# Update table with each update
def draw_table(x, y, z, table):
    while True:
        time.sleep(60)
        os.system('clear')

        # First 5 entries of table
        if len(x) % 5 != 0 and len(x) % 30 != 0:
            table.add_row([len(x), round(x[-1], 2), '', ''])

        # Remaining entries
        elif len(x) % 5 == 0 and len(x) % 30 == 0:
            table.add_row([len(x), round(x[-1], 2), round(y[-1], 2), round(z[-1], 2)])
        
        elif len(x) % 5 == 0 and len(x) % 30 != 0:
            table.add_row([len(x), round(x[-1], 2), round(y[-1], 2), ''])

        elif len(x) % 5 != 0 and len(x) % 30 == 0:
            table.add_row([len(x), round(x[-1], 2), '', round(y[-1], 2)])

        print(table)


if __name__ == "__main__":
    main()
