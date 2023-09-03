import time 
import requests
import socket
import datetime



print("This prorgram will querry a service and an DNS name, compare them and return wether the record should be updated")
print("Started : " + str(datetime.datetime.today()) + "\n~~~~~~~~~~~")
link = 'https://checkip.amazonaws.com'
link2 = 'home.techtinkerhub.com'

while True:
	recordIP = socket.gethostbyname(link2)
	ip = requests.get(link).text.strip()
	if(recordIP != ip):
		print("Ip should be updated from :" + str(recordIP) + " to " + str(ip))
	time.sleep(3600)

