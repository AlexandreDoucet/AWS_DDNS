# DDNS Service with Python and Docker
This GitHub repository contains a Python script and Docker configuration to simulate the functionalities of a Dynamic Domain Name System (DDNS) service that updates records stored on AWS Route 53. This service periodically checks for changes in your external IP address and updates the corresponding DNS record if necessary. Below, you'll find instructions on how to use this code and set up the Docker container.

## Prerequisites
Before running the DDNS service, make sure you have the following prerequisites installed:

- [Docker](https://www.docker.com/)
- [Python](https://www.python.org/)
- [AWS CLI](https://aws.amazon.com/cli/)
- An AWS Route 53 hosted zone set up with the domain you want to update.
- An AWS IAM user configures with permission for Route 53.
- An Understanding of how to create and run docker containers.

## Getting Started
1. Clone this GitHub repository to your local machine:</br>
```git clone https://github.com/AlexandreDoucet/AWS_DDNS.git```

1. Navigate to the project directory:</br>
```cd ddns-service```

1. Build the Docker container using the provided Dockerfile:</br>
```docker build -t ddns-service .```

## Configuration

### Environment Variables
Before running the Docker container, you need to set the following environment variables in the Docker runtime. You can do this by creating an .env file or by passing these variables directly to the docker run command:
</br>Please note that having the IAM_KEY set as en evironenemnt variable is not very secure but will do for now.

#### Passing variables directly to the docker run command :
```
docker run -e DOMAIN="DOMAIN_TO_COMPARE_AND_UPDATE_TO" \
	   -e HOSTED_ZONE_ID="your-hosted-zone-id" \
	   -e IAM_USER="iam-user-access-key" \
	   -e IAM_KEY="Your AWS IAM user secret key" \
	   -e SCHEDULED_TIME="00:00" \
	   -e AWS_PROFILE_NAME="myprofile" \
	   --restart=always \
	   --name CompareDNS \
	   -d \
	   --log-driver json-file \
	   --log-opt max-size=10m \
	   --log-opt max-file=3 \
	   compare_dns
```
HOSTED_ZONE_ID: Your AWS Route 53 hosted zone ID.</br>
IAM_USER: Your AWS IAM user access key.</br>
IAM_KEY: Your AWS IAM user secret key.</br>
SCHEDULED_TIME: The time at which you want the code to run in HH:MM format.</br>
DOMAIN: The domain you want to update in your Route 53 hosted zone.</br>
AWS_PROFILE_NAME: An optional AWS CLI profile name (default is "myprofile").</br>
	
#### Example .env File
Create an .env file in the project directory with the following content:

HOSTED_ZONE_ID=your-hosted-zone-id</br>
IAM_USER=your-iam-user-access-key</br>
IAM_KEY=your-iam-user-secret-key</br>
SCHEDULED_TIME=00:00</br>
DOMAIN=your-domain.com</br>
AWS_PROFILE_NAME=myprofile</br>
Running the DDNS Service</br>

Run the Docker container with the following command, ensuring that you mount the AWS CLI configuration and credentials files:
```
docker run --restart=always \
	   --name CompareDNS \
	   -d \
	   --env-file .env \
	   --log-driver json-file \
	   --log-opt max-size=10m \
	   --log-opt max-file=3 \
	   compare_dns
```
This command does the following:

	-d: Runs the container in detached mode.
	--name ddns-service: Assigns a name to the running container.
	--env-file .env: Reads environment variables from the .env file.
	ddns-service: The name of the Docker image.

## Monitoring
The DDNS service will run periodically based on the SCHEDULED_TIME specified in your environment variables. If no time is specifide or the format is invalid, it will default as 00:00 (Midnight)
You can monitor the service's logs to see if it's updating the DNS records correctly:

	docker logs -f compare_dns 

##Contributing
Feel free to contribute to this project by opening issues or submitting pull requests. Your contributions are welcome!












