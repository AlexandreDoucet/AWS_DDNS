import time 
import requests
import socket
import datetime
import subprocess
import os

#subprocess.call(['aws','configure'])

def check_internet_connection():
    try:
        # Use the ping command to check if a well-known website is reachable
        subprocess.check_call(["ping", "-c", "1", "www.google.com"])
        return True
    except subprocess.CalledProcessError:
        return False

def get_aws_profile_info():
	aws_user = os.environ.get("IAM_USER")
	aws_key = os.environ.get("IAM_KEY")
	return aws_user, aws_key

def create_aws_profile(aws_user, aws_key):
	try:
		# Use subprocess to execute the aws configure set commands.
		subprocess.run(["aws", "configure", "set", "aws_access_key_id", aws_user, "--profile", "myprofile"])
		subprocess.run(["aws", "configure", "set", "aws_secret_access_key", aws_key, "--profile", "myprofile"])
		print("AWS profile 'myprofile' created successfully.")
	except Exception as e:
		print(f"Failed to create AWS profile: {str(e)}")


time_to_wait = 20
alreadyPrinted = False
while True:

	if check_internet_connection() :
		print("Internet connection is available.")
		break
	else:
		if not alreadyPrinted:
			print("No internet available\r\t\t\t\r")
			alreadyPrinted = True
		time.sleep(time_to_wait)

try:
	subprocess.check_call(['aws', 'configure', 'get', 'aws_access_key_id'])
	print("AWS CLI is already configured with IAM credentials.")
except subprocess.CalledProcessError:
	print("AWS CLI is not configured. Running 'aws configure'...")

	aws_user, aws_key = get_aws_profile_info()

	if aws_user and aws_key:
		print("Using AWS credentials from environment variables.")
		create_aws_profile(aws_user, aws_key)
	else:
		print("AWS_USER and/or AWS_KEY environment variables not set. Please set them or run 'aws configure' manually.")
		print("AWS CLI is not configured. Running 'aws configure'...")
		subprocess.call(['aws', 'configure'])


print("\n\nThis prorgram will querry a service and an DNS name, compare them and return wether the record should be updated")
print("Started : " + str(datetime.datetime.today()) + "\n~~~~~~~~~~~")
link = 'https://checkip.amazonaws.com'
link2 = 'home.techtinkerhub.com'

delay = float(os.environ.get("SYNC_INTERVAL_SECONDS"))
uploadScript = 'UploadToAWS.sh'

recordIP = '0.0.0.0'

lastIP = ""
last_check_time = time.time()
delay_seconds = delay


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
