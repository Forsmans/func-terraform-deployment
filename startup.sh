#!/bin/bash

# Install Git
apt-get update && apt-get install -y git

# Install Terraform (if needed)
TERRAFORM_VERSION="1.5.7"
wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/local/bin/
rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip