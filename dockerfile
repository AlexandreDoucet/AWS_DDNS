FROM python:latest

WORKDIR /project

run pip install -U \
pip \
setuptools \
wheel

run apt-get update && apt-get install -yy less
run apt install unzip
run apt-get install -y iputils-ping

run ln -sf /usr/share/zoneinfo/America/Moncton /etc/timezone
run ln -sf /usr/share/zoneinfo/America/Moncton /etc/localtime

run curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
run unzip awscliv2.zip
run ./aws/install

copy /source/requirements.txt .
run pip install -r requirements.txt


# Define an argument to pass HOSTED_ZONE_ID during runtime
ARG HOSTED_ZONE_ID
ARG IAM_USER
ARG IAM_KEY


# Set the HOSTED_ZONE_ID as an environment variable
ENV HOSTED_ZONE_ID=${HOSTED_ZONE_ID}
ENV IAM_USER=${IAM_USER}
ENV IAM_KEY=${IAM_KEY}


copy /source .

run chmod +x UploadToAWS.sh


cmd ["python","-u","main.py"]
