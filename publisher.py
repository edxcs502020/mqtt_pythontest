# Python application to publish pseudorandom numbers to MQTT message broker

import paho.mqtt.client as mqtt
import random
import time

def main():
    mqtt_client = mqtt.Client()
    # keepalive=30 to match largest interval
    mqtt_client.connect("localhost", 1883, 30)

    while True:
        # Interval to generate pseudorandom number
        time.sleep(random.randint(1,30))

        # Number to be generated
        rand_num = random.randint(1, 100)
        mqtt_client.publish("topic/rand_num", rand_num)

    mqtt_client.disconnect();

if __name__ == "__main__":
    main()