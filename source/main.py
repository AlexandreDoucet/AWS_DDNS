import time 
import requests
import socket
import datetime
import subprocess


#subprocess.call(['aws','configure'])

def check_internet_connection():
    try:
        # Use the ping command to check if a well-known website is reachable
        subprocess.check_call(["ping", "-c", "1", "www.google.com"])
        return True
    except subprocess.CalledProcessError:
        return False


while True:
    timeToWait = 10
    if check_internet_connection():
        print("Internet connection is available.")
        break
    else:
        print("No internet connection. Waiting for "+str(timeToWait)+" seconds...")
        time.sleep(timeToWait)



# Check if AWS CLI is already configured
try:
    subprocess.check_call(['aws', 'configure', 'get', 'aws_access_key_id'])
    print("AWS CLI is already configured with IAM credentials.")
except subprocess.CalledProcessError:
    print("AWS CLI is not configured. Running 'aws configure'...")
    subprocess.call(['aws', 'configure'])

print("This prorgram will querry a service and an DNS name, compare them and return wether the record should be updated")
print("Started : " + str(datetime.datetime.today()) + "\n~~~~~~~~~~~")
link = 'https://checkip.amazonaws.com'
link2 = 'home.techtinkerhub.com'

uploadScript = 'UploadToAWS.sh'

recordIP = '0.0.0.0'

lastIP = ""
last_check_time = time.time()
delay_seconds = 3600


while True:
	ip = requests.get(link).text.strip()
	current_time = time.time()
    
    # Check if the IP has changed or an hour has passed
	if lastIP != ip or (current_time - last_check_time) >= delay_seconds:  # 3600 seconds = 1 hour
		# Polled IP has changed or an hour has passed
		print('\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
		recordIP = socket.gethostbyname(link2)
		lastIP = ip
		last_check_time = current_time

		if recordIP != ip:
			print("IP should be updated from :" + str(recordIP) + " to " + str(ip))
			subprocess.call(['sh', uploadScript])
			print("Record Updated : " + str(datetime.datetime.today()))
			time.sleep(1)
		else:
			print("No update required : " + str(datetime.datetime.today()))

		print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n')
	else:
        	time.sleep(60)
