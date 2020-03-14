from flask import Flask, app, request
from logger import logger
import json.tool
import os
app = Flask(__name__)

audit_log_server_ip = os.environ.get('MY_HOST', default="localhost")
audit_log_server_port = os.environ.get('MY_PORT', default=44416)
redis_host = os.environ.get("REDIS_HOST", default="localhost")
redis_port = os.environ.get("REDIS_PORT", default=6379)

logger_instance = None

@app.route("/getCurrentTransactionNum", methods=["POST"])
def get_current_transaction_num():
    current_transaction_num = logger_instance.get_current_transaction_num()
    return json.dumps({"status": "SUCCESS", "data": current_transaction_num})

@app.route("/getNextTransactionNum", methods=["POST"])
def get_next_transaction_num():
    next_transaction_num = logger_instance.get_next_transaction_num()
    logger_instance.increment_transaction_num()
    return json.dumps({"status": "SUCCESS", "data": next_transaction_num})

@app.route("/auditLog", methods=["POST"])
def insert_log():
    data = request.json
    response = logger_instance.insert_log(data)
    return json.dumps(response)

@app.route("/dumpLog", methods=["POST"])
def get_logs():
    data = request.json
    response = logger_instance.get_logs(data)
    return json.dumps(response)

@app.route("/debug", methods=["GET"])
def debug():
    audit_log = logger_instance.debug()
    return json.dumps({"status": "SUCCESS", "data": audit_log})

if __name__ == "__main__":
    logger_instance = logger(redis_host=redis_host, redis_port=redis_port)
    app.run(host=audit_log_server_ip, port=audit_log_server_port)