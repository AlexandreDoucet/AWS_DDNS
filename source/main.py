import time
import requests
import socket
import datetime
import subprocess
import os
import logging

# Configuration
CONFIG = {
	"SYNC_INTERVAL_SECONDS": float(os.environ.get("SYNC_INTERVAL_SECONDS", 3600)),
	"AWS_PROFILE_NAME": "myprofile",
	"UPLOAD_SCRIPT": "UploadToAWS.sh",
}


link = 'https://checkip.amazonaws.com'
domain = os.environ.get("DOMAIN", 'home.techtinkerhub.com') 


# Logging configuration
logging.basicConfig(filename="ip_updater.log", level=logging.INFO)

def check_internet_connection():
	try:
		subprocess.check_call(["ping", "-c", "1", "www.google.com"])
		return True
	except subprocess.CalledProcessError:
		return False

# Causes the program to stall if the internet is down.
def wait_for_internet_connection():
	time_to_wait = 20
	already_printed = False
	
	while True:
		if check_internet_connection():
			logging.info("Internet connection is available.")
			break
		else:
			if not already_printed:
				logging.warning("No internet available")
				already_printed = True
			time.sleep(time_to_wait)

def get_aws_profile_info():
	aws_user = os.environ.get("IAM_USER")
	aws_key = os.environ.get("IAM_KEY")
	return aws_user, aws_key

def create_aws_profile(aws_user, aws_key):
	try:
		subprocess.run(["aws", "configure", "set", "aws_access_key_id", aws_user, "--profile", AWS_PROFILE_NAME])
		subprocess.run(["aws", "configure", "set", "aws_secret_access_key", aws_key, "--profile", AWS_PROFILE_NAME])
		logging.info("AWS profile '%s' created successfully.", AWS_PROFILE_NAME)
	except Exception as e:
		logging.error("Failed to create AWS profile: %s", str(e))

def validate_aws_profile():
	aws_key_valid = False
	while not aws_key_valid:
		try:
			subprocess.check_call(["aws", "configure", "get", "aws_access_key_id"])
			logging.info("AWS CLI is already configured with IAM credentials.")
			aws_key_valid = True  # The key is valid, exit the loop
		except subprocess.CalledProcessError:
			logging.warning("AWS CLI is not configured.")

			aws_user, aws_key = get_aws_profile_info()			
			if aws_user and aws_key:
				logging.info("Using AWS credentials from environment variables.")
				create_aws_profile(aws_user, aws_key)
				aws_key_valid = True  # The key is now configured, exit the loop
			else:
				logging.error("AWS_USER and/or AWS_KEY environment variables not set.")
				logging.warning("AWS CLI is not configured. Running 'aws configure'...\n")
				subprocess.call(["aws", "configure"])



def main():

	wait_for_internet_connection()
	validate_aws_profile()

	logging.info("\nProgram started: %s", str(datetime.datetime.today()))

	record_ip = '0.0.0.0'
	last_ip = ""
	last_check_time = time.time()
	delay_seconds = CONFIG["SYNC_INTERVAL_SECONDS"]

	while True:
		wait_for_internet_connection()

		ip = requests.get(link).text.strip()
		current_time = time.time()

		if last_ip != ip or (current_time - last_check_time) >= delay_seconds:
			logging.info("IP change detected or interval passed.")
			record_ip = socket.gethostbyname(domain)
			last_ip = ip
			last_check_time = current_time

			if record_ip != ip:
				logging.info("IP should be updated from: %s to %s", record_ip, ip)
				subprocess.call(["sh", UPLOAD_SCRIPT])
				logging.info("Record Updated: %s", str(datetime.datetime.today()))
				time.sleep(1)
			else:
				logging.info("No update required: %s", str(datetime.datetime.today()))

		time.sleep(120)

if __name__ == "__main__":
	main()
