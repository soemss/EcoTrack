from flask import Flask
from methods import *
import socket
import subprocess
import json


port = 8000
app = Flask(__name__)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(('8.8.8.8', 1))
local_ip_address = sock.getsockname()[0]
with open("server_info.txt", "w+") as file:
    file.write(f"http://{local_ip_address}:{port}")

@app.route('/alerts/<zipcode>', methods = ['GET'])
def alerts(zipcode):
    zipcode = int(zipcode)
    county, state = zip_to_county_name(zipcode)
    link = county_warnings_link(county, state)
    dict_of_alerts = all_alerts(link)
    return dict_of_alerts

@app.route("/members")
def members():
    return {"members" : ["Member1", "Member2", "Member3"]}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)