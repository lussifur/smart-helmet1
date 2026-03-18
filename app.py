from flask import Flask, jsonify
from flask_cors import CORS
from azure.eventhub import EventHubConsumerClient
import json
import threading

app = Flask(__name__)
CORS(app)

# 🔥 GLOBAL DATA STORAGE
latest_data = {}

# 🔑 Azure Event Hub connection (PASTE YOUR VALUE)
EVENT_HUB_CONNECTION_STR = "Endpoint=sb://ihsuprodsgres008dednamespace.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=ae+rWHbKDwUYJL1SHFtN8VWT2Uf840yXoAIoTCemBeg=;EntityPath=iothub-ehub-smart-helm-57807286-1ec8c9a59c"
CONSUMER_GROUP = "$Default"

# 🚀 FUNCTION: Receive data from Azure
def on_event(partition_context, event):
    global latest_data
    try:
        data = event.body_as_str()
        latest_data = json.loads(data)

        print("📡 Data from Azure:", latest_data)

    except Exception as e:
        print("Error:", e)

# 🚀 START LISTENER
def start_listener():
    client = EventHubConsumerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR,
        consumer_group=CONSUMER_GROUP
    )

    with client:
        client.receive(
            on_event=on_event,
            starting_position="-1"   # read latest data
        )

# 🧵 RUN LISTENER IN BACKGROUND
threading.Thread(target=start_listener, daemon=True).start()

# 🌐 ROUTES
@app.route('/')
def home():
    return "Azure Smart Helmet Server Running 🚀"

@app.route('/data')
def get_data():
    return jsonify(latest_data)

# 🚀 RUN SERVER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)