import time
import requests
import socket
import datetime
import subprocess
import os
import schedule

# Configuration
CONFIG = {
	"SCHEDULED_TIME": str(os.environ.get("SCHEDULED_TIME", "00:00").strip()),
	"AWS_PROFILE_NAME": os.environ.get("AWS_PROFILE_NAME", "myprofile"),
	"UPLOAD_SCRIPT": "UploadToAWS.sh",
}


link = 'https://checkip.amazonaws.com'
domain = os.environ.get("DOMAIN", 'home.techtinkerhub.com') 


# Logging configuration
#logging.basicConfig(filename="ip_updater.log", level=logging.INFO)

def check_internet_connection():
	result = False
	try:
		subprocess.check_call(["ping", "-c", "1", "www.google.com"], stdout=subprocess.DEVNULL)
		result = True
	except subprocess.CalledProcessError:
		result = False
	return result

# Causes the program to stall if the internet is down.
def wait_for_internet_connection(quiet):
	time_to_wait = 20
	already_printed = False	
	while True:
		if check_internet_connection():
			
			if(not quiet): print("Internet connection is available : " +str(datetime.datetime.today()))
			break
		else:
			if not already_printed:
				print("No internet available : " + str(datetime.datetime.today()))
				already_printed = True
			time.sleep(time_to_wait)

def get_aws_profile_info():
	aws_user = os.environ.get("IAM_USER")
	aws_key = os.environ.get("IAM_KEY")
	return aws_user, aws_key

def create_aws_profile(aws_user, aws_key):
	try:
		subprocess.run(["aws", "configure", "set", "aws_access_key_id", aws_user, "--profile", CONFIG["AWS_PROFILE_NAME"]])
		subprocess.run(["aws", "configure", "set", "aws_secret_access_key", aws_key, "--profile", CONFIG["AWS_PROFILE_NAME"]])
		print("AWS profile "+ CONFIG["AWS_PROFILE_NAME"] +" created successfully.")
	except Exception as e:
		print("Failed to create AWS profile: " + str(e))

	aws_key_valid = False
	while not aws_key_valid:
		try:
			subprocess.check_call(["aws", "--profile", CONFIG["AWS_PROFILE_NAME"], "configure", "get", "aws_access_key_id"],stdout=subprocess.DEVNULL)
			print("AWS CLI is already configured with IAM credentials.")
			aws_key_valid = True  # The key is valid, exit the loop
		except subprocess.CalledProcessError:
			print("AWS CLI is not configured.")

			aws_user, aws_key = get_aws_profile_info()			
			if aws_user and aws_key:
				print("Using AWS credentials from environment variables.")
				create_aws_profile(aws_user, aws_key)
				aws_key_valid = True  # The key is now configured, exit the loop
			else:
				print("AWS_USER and/or AWS_KEY environment variables not set.")
				print("AWS CLI is not configured. Running 'aws configure'...\n")
				subprocess.call(["aws", "configure"])




def run_job(mut_last_ip, forceCheck):
	wait_for_internet_connection(True)
	ip = requests.get(link).text.strip()
	last_ip = mut_last_ip[0].strip()

	if last_ip != ip or forceCheck:
		if(last_ip != ip ):
			print("IP change detected")
		elif(forceCheck):
			print("Scheduled update")

		record_ip = socket.gethostbyname(domain)
		print("Current record IP : " + record_ip)
		print("Current Querry ip : " + ip)
		if record_ip != ip:
			print("IP should be updated from:" + str(record_ip) + " to " + str(ip))
			subprocess.call(["sh", CONFIG["UPLOAD_SCRIPT"]])
			print("Record Updated: " + str(datetime.datetime.today()))
			time.sleep(20)
		else:
			print("No update required : " + str(datetime.datetime.today()))
		print("\n")
		mut_last_ip[0] = ip




def main():

	print("\nProgram started: " + str(datetime.datetime.today()))
	wait_for_internet_connection(False)
	aws_user,aws_key = get_aws_profile_info()
	create_aws_profile(aws_user, aws_key)

	last_ip = [str("")]

	# Define the specific time you want the code to run (replace with your desired time).
	scheduled_time = CONFIG["SCHEDULED_TIME"].strip()  # Replace with your desired time in HH:MM format.

	# Schedule the job to run at the specified time.
	try:
		schedule.every().day.at(scheduled_time).do(run_job,last_ip,True)
	except Exception as e:
		scheduled_time="00:00"
		schedule.every().day.at(scheduled_time).do(run_job,last_ip,True)
		print(e)
		print(type(e))
		print("\n\n")


	schedule.every(2).minutes.do(run_job,last_ip,False)

	print("\nLooks like we're good to do !\n")
	schedule.run_all()
	while True:
		time.sleep(20)
		schedule.run_pending()


if __name__ == "__main__":
	main()
