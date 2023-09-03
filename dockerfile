FROM python:latest

WORKDIR /project

run pip install -U \
pip \
setuptools \
wheel

run ln -sf /usr/share/zoneinfo/America/Moncton /etc/timezone
run ln -sf /usr/share/zoneinfo/America/Moncton /etc/localtime


copy /source/requirements.txt .
run pip install -r requirements.txt


copy /source .


cmd ["python","-u","main.py"]
