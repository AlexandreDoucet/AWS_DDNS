import time 
import requests
import socket
import datetime
import subprocess

subprocess.call(['aws','configure'])

print("This prorgram will querry a service and an DNS name, compare them and return wether the record should be updated")
print("Started : " + str(datetime.datetime.today()) + "\n~~~~~~~~~~~")
link = 'https://checkip.amazonaws.com'
link2 = 'home.techtinkerhub.com'

uploadScript = 'UploadToAWS.sh'

recordIP = '0.0.0.0'

while True:
	ip = requests.get(link).text.strip()

	if(recordIP != ip):
		recordIP = socket.gethostbyname(link2)
		print("Ip should be updated from :" + str(recordIP) + " to " + str(ip))
		subprocess.call(['sh',uploadScript])
		time.sleep(1)
	else:
		print("No update required : " + datetime.datetime.today())
	time.sleep(3600)

