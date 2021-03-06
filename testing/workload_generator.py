import sys
import socket
import requests
import json
from enum_utils import CommandURLs
import os
from dotenv import load_dotenv
BUFFER_SIZE = 4096

# command line usage: "py workload_generator.py --1"
# Where '--1' is the workload file to use as stated below

load_dotenv()
load_balancer_ip = os.environ.get("load_balancer_host")
load_balancer_port = int(os.environ.get("load_balancer_port"))
protocol = "http"
load_balancer_url = f"{protocol}://{load_balancer_ip}:{load_balancer_port}"

workload_paths = {
    "--1": "./workload_files/1userWorkLoad.txt",
    "--2": "./workload_files/2userWorkLoad.txt",
    "--10": "./workload_files/10User_testWorkLoad.txt",
    "--45": "./workload_files/45User_testWorkLoad.txt",
    "--100": "./workload_files/100User_testWorkLoad.txt",
    "--1000": "./workload_files/1000User_testWorkLoad.txt",
    "--2006": "./workload_files/final2006WorkLoad.txt",
    "--2007": "./workload_files/final2007.txt",
    "--2009": "./workload_files/final_workload_2009.txt",
    "--2010": "./workload_files/final_workload_spring_2010.txt",
    "--2011": "./workload_files/final_workload_2011.txt",
    "--2013": "./workload_files/final_workload_2013.txt",
    "--2014": "./workload_files/final_workload_2014.txt",
    "--2015": "./workload_files/final_workload_2015.txt",
    "--2016": "./workload_files/2016.txt",
    "--2017": "./workload_files/final_workload_2017.txt",
    "--2018": "./workload_files/final_workload_2018.txt",
    "--2019": "./workload_files/final_workload_2019.txt",
}

def process_dumplog(output_filename, dumplog_response):
    try:
        xml_string = json.loads(dumplog_response)["data"]
        with open(output_filename, 'w+') as f:
            f.write(xml_string)
    except KeyError:
        print(f"Error: no data attribute found in response. Response status {json.loads(dumplog_response)['status']}")

# Read work load file, process into dict commands
def run_commands(file_obj):
    client_actions_raw = [line.rstrip().split()[-1].split(",") for line in file_obj]
    for i, action in enumerate(client_actions_raw):
        command = action[0]
        next_command = {"Command": command}
        try:
            if command == "ADD":
                next_command["userid"] = action[1]
                next_command["amount"] = action[2]
            elif command == "QUOTE":
                next_command["userid"] = action[1]
                next_command["StockSymbol"] = action[2]
            elif command == "BUY":
                next_command["userid"] = action[1]
                next_command["StockSymbol"] = action[2]
                next_command["amount"] = action[3]
            elif command == "COMMIT_BUY":
                next_command["userid"] = action[1]
            elif command == "CANCEL_BUY":
                next_command["userid"] = action[1]
            elif command == "SELL":
                next_command["userid"] = action[1]
                next_command["StockSymbol"] = action[2]
                next_command["amount"] = action[3]
            elif command == "COMMIT_SELL":
                next_command["userid"] = action[1]
            elif command == "CANCEL_SELL":
                next_command["userid"] = action[1]
            elif command == "SET_BUY_AMOUNT":
                next_command["userid"] = action[1]
                next_command["StockSymbol"] = action[2]
                next_command["amount"] = action[3]
            elif command == "CANCEL_SET_BUY":
                next_command["userid"] = action[1]
                next_command["StockSymbol"] = action[2]
            elif command == "SET_BUY_TRIGGER":
                next_command["userid"] = action[1]
                next_command["StockSymbol"] = action[2]
                next_command["amount"] = action[3]
            elif command == "SET_SELL_AMOUNT":
                next_command["userid"] = action[1]
                next_command["StockSymbol"] = action[2]
                next_command["amount"] = action[3]
            elif command == "CANCEL_SET_SELL":
                next_command["userid"] = action[1]
                next_command["StockSymbol"] = action[2]
            elif command == "SET_SELL_TRIGGER":
                next_command["userid"] = action[1]
                next_command["StockSymbol"] = action[2]
                next_command["amount"] = action[3]
            elif command == "DISPLAY_SUMMARY":
                next_command["userid"] = action[1]
            elif command == "DUMPLOG":
                filenameIndex = 1
                usernameIndex = None
                if (len(action) == 3):
                    filenameIndex = 2
                    usernameIndex = 1
                next_command["filename"] = action[filenameIndex]
                if (usernameIndex != None):
                    next_command["userid"] = action[usernameIndex]
            else:
                print(f"Invalid command: #{i + 1} -> {action}")
                continue
        except Exception as e:
            print(f"{e} | {action}")
            continue

        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sckt.connect((load_balancer_ip, load_balancer_port))
        data = json.dumps(next_command)
        http_request = f"POST {CommandURLs[command].value} HTTP/1.1\nHOST: {load_balancer_ip}:{load_balancer_port}\nContent-Type: application/json\nAccept: application/json\n{data}"
        sckt.sendall(str.encode(http_request))
        server_response = sckt.recv(BUFFER_SIZE).decode()
        #server_response = requests.post((load_balancer_url + CommandURLs[command].value), data=next_command)
        print(f"#{i + 1} action:{action} response:{server_response}")

        try:
            process_dumplog(next_command["filename"], server_response)
        except KeyError:
            pass


# TEMPORARY: for dumplog development--------
# 	audit_log_server_ip = "localhost"  # IP on home comp
# 	audit_log_server_port = 44416
# 	protocol = "http"
# 	from AuditLogBuilder import AuditLogBuilder
# 	import json
# 	server_name = "someserver"
# 	request_dict1 = json.dumps({
# 		"Command": "ADD",
# 		"userid": "someUserGuy",
# 		"amount": 100.10
# 	})
# 	AuditLogBuilder("ADD", server_name).build(request_dict1).send(protocol, audit_log_server_ip, audit_log_server_port)
# 	request_dict2 = json.dumps({
# 		"Command": "ADD",
# 		"userid": "someUserGuy2",
# 		"amount": 100.10
# 	})
# 	AuditLogBuilder("ADD", server_name).build(request_dict2).send(protocol, audit_log_server_ip, audit_log_server_port)
# 	#-------------------------------------------

if __name__ == "__main__":
    file_index = sys.argv[1]
    file_object = open(workload_paths[file_index])
    run_commands(file_object)
