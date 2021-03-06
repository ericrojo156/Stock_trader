from flask import Flask, app, request
from event_messenger import event_messenger
import json.tool
import os

app = Flask(__name__)

redis_host = os.environ['REDIS_HOST']
redis_port = int(os.environ['REDIS_PORT'])
event_messenger_ip = os.environ['MY_EVENT_HOST']
event_messenger_port = int(os.environ['MY_EVENT_PORT'])

event_messenger_instance = None

print("redis host = " + str(redis_host))


@app.route("/set_event", methods=["POST"])
def set_event():
    data = request.json
    username = data["username"]
    stock_symbol = data["stock_symbol"]
    target_dollars = data["target_dollars"]
    target_cents = data["target_cents"]
    event_type = data["event_type"]
    response = event_messenger.set_event(event_type, username, stock_symbol, target_dollars, target_cents)
    return json.dumps(response)


@app.route("/set_event_status")
def set_event_status():
    data = request.json
    event_id = data["event_id"]
    new_status = data["new_status"]
    response = event_messenger.set_event_status(event_id, new_status)
    return json.dumps(response)


@app.route("/delete_event")
def delete_event():
    data = request.json
    response = event_messenger.delete_event(data["event_id"])
    return json.dumps(response)


if __name__ == "__main__":
    event_messenger_instance = event_messenger(redis_host=redis_host, redis_port=redis_port)
    app.run(host=event_messenger_ip, port=event_messenger_port)
