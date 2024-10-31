import json
import struct
import paho.mqtt.client as mqtt

# MQTT configuration
IO_LINK_BROKER = "192.168.1.125"  # Replace with the actual IP or hostname
IO_LINK_PORT = 1883  # Default MQTT port

YOUSSEF_BROKER = "192.168.1.124"  # Replace with the actual IP or hostname
YOUSSEF_PORT = 1883  # Default MQTT port

INPUT_TOPIC = "io_link/data"  # Topic to subscribe to for receiving raw data
OUTPUT_TOPIC = "processed/data"  # Topic to publish transformed data to

# Function to decode raw bytes from the hex data
def decode_data(raw_bytes):
    decoded_values = {}
    # Decode each IN-WORD as per the mapping
    decoded_values['V.Rms'] = struct.unpack('>H', raw_bytes[0:2])[0] * 0.0001
    decoded_values['A.Peak'] = struct.unpack('>H', raw_bytes[4:6])[0] * 0.1
    decoded_values['A.Rms'] = struct.unpack('>H', raw_bytes[8:10])[0] * 0.1
    decoded_values['Temperature'] = struct.unpack('>H', raw_bytes[12:14])[0] * 0.1
    decoded_values['A.Crest'] = struct.unpack('>H', raw_bytes[16:18])[0] * 0.1
    decoded_values['DeviceStatus'] = struct.unpack('>H', raw_bytes[18:20])[0]

    return decoded_values

# MQTT callback function for when a message is received
def on_message(client, userdata, msg):
    print("Received message from IO-Link MQTT Broker")
    # Parse the JSON payload
    payload = json.loads(msg.payload)
    hex_data = payload["data"]["payload"]["/iolinkmaster/port[3]/iolinkdevice/pdin"]["data"]
    raw_bytes = bytes.fromhex(hex_data)

    # Decode the data
    decoded_values = decode_data(raw_bytes)
    
    # Prepare the data for publishing
    transformed_payload = {
        "code": "processed_event",
        "data": decoded_values
    }

    # Publish to Youssef's MQTT Broker
    client_youssef.publish(OUTPUT_TOPIC, json.dumps(transformed_payload))
    print(f"Transformed data sent to Youssef's MQTT Broker: {transformed_payload}")

# Initialize MQTT clients for both brokers
client_io_link = mqtt.Client(client_id="io_link_client")
client_youssef = mqtt.Client(client_id="youssef_client")

# Configure connection to IO-Link MQTT Broker
client_io_link.on_message = on_message
client_io_link.connect(IO_LINK_BROKER, IO_LINK_PORT)
client_io_link.subscribe(INPUT_TOPIC)

# Connect to Youssef's MQTT Broker
client_youssef.connect(YOUSSEF_BROKER, YOUSSEF_PORT)

# Start loop to process MQTT messages
client_io_link.loop_start()
client_youssef.loop_start()

print("Listening for messages from IO-Link MQTT Broker...")
try:
    while True:
        pass  # Keep the script running
except KeyboardInterrupt:
    print("Stopping the MQTT clients...")
finally:
    client_io_link.loop_stop()
    client_youssef.loop_stop()
    client_io_link.disconnect()
    client_youssef.disconnect()
