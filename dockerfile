FROM python:latest

WORKDIR /project

run pip install -U \
pip \
setuptools \
wheel

run apt install unzip
run apt-get update && apt-get install -yy less


run ln -sf /usr/share/zoneinfo/America/Moncton /etc/timezone
run ln -sf /usr/share/zoneinfo/America/Moncton /etc/localtime

run curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
run unzip awscliv2.zip
run ./aws/install

copy /source/requirements.txt .
run pip install -r requirements.txt

copy /source .

run chmod +x UploadToAWS.sh


cmd ["python","-u","main.py"]
