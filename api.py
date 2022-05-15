import socket
from flask import Flask, request

# Flask boiler-plate
app = Flask(__name__)

ip_host = "192.168.0.110"
ip_port = 65432
ip_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_sock.connect((ip_host, ip_port))

def send_message(msg):
    ip_sock.send(msg.encode())
    data = ip_sock.recv(1024)
    
    if data != None: print("<< {0}".format(data))

    return { "response": data }
    
@app.route('/rotate', methods=['POST'])
def forward():
    return send_message("rotate")

@app.route('/stop', methods=['POST'])
def stop():
    return send_message("stop")

@app.route('/adjust', methods=['POST'])
def adjust():
    res = request.get_json()
    a = res["power"]
    return send_message("adjust {0}".format(a))

@app.route('/temp', methods=['GET'])
def temp():
    result = send_message("read_temp")
    return { "temperature": float(result["response"].decode('utf-8')) }

@app.route('/power', methods=['GET'])
def power():
    result = send_message("read_power")
    return { "power": float(result["response"].decode('utf-8')) }

if __name__ == '__main__':
    app.run(threaded=False)