from motor import Motor
from pwm import PWM
from pin import Pin
from pickle import FALSE
import socket
from utils import power_read, cpu_temperature

ip_host = "192.168.0.110"
ip_port = 65432
backlog = 1

ip_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_sock.bind((ip_host, ip_port))
ip_sock.listen(backlog)

print("listening on port ", ip_port)
client, clientInfo = ip_sock.accept()

# Init motors
motor = Motor(PWM("P13"), Pin("D4")) # motor 1
power = 50

def rotate():
	motor.set_power(power)

def stop():
    motor.set_power(0)

def set_motor_power(new_power):
    global power
    power = new_power * 50

######################################################## 

while 1:
	print("server recv from: ", clientInfo)
	result = None
	data = client.recv(1024)
	if data is None: continue

	data= str(data.decode("utf-8"))
	args = data.split(' ')
	command = args[0]

	if command == "rotate":
		rotate()
		result = True

	elif command == "adjust":
		parsed_arg = int(args[1])
		set_motor_power(parsed_arg)
		result = True

	elif command == "stop":
		stop()
		result = True
	
	elif command == "read_power":
		result = power_read()
	
	elif command == "read_temp":
		result = cpu_temperature()

	client.send(str(result).encode('utf-8'))