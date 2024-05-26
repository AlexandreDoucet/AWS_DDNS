FROM python:latest

WORKDIR /project

# Upgrade pip, setuptools, and wheel
RUN pip install -U \
    pip \
    setuptools \
    wheel

# Install required packages
RUN apt-get update && \
    apt-get install -yy less unzip iputils-ping

# Set timezone
RUN ln -sf /usr/share/zoneinfo/America/Moncton /etc/timezone && \
    ln -sf /usr/share/zoneinfo/America/Moncton /etc/localtime

# Download and install AWS CLI for x86_64
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install

# Copy requirements and install dependencies
COPY /source/requirements.txt .
RUN pip install -r requirements.txt

# Define arguments to pass during build time
ARG HOSTED_ZONE_ID
ARG IAM_USER
ARG IAM_KEY
ARG SCHEDULED_TIME
ARG DOMAIN
ARG AWS_PROFILE_NAME

# Set environment variables
ENV HOSTED_ZONE_ID=${HOSTED_ZONE_ID}
ENV IAM_USER=${IAM_USER}
ENV IAM_KEY=${IAM_KEY}
ENV SCHEDULED_TIME=${SCHEDULED_TIME}
ENV DOMAIN=${DOMAIN}
ENV AWS_PROFILE_NAME=${AWS_PROFILE_NAME}

# Copy project files
COPY /source .

# Make script executable
RUN chmod +x UploadToAWS.sh

# Set the entrypoint
CMD ["python", "-u", "main.py"]
