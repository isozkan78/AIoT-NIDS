
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    print(f"⚠️ Uyarı Alındı: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = lambda c, u, f, rc: client.subscribe("aiot-nids/alert")
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()
