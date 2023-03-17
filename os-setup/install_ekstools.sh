#!/bin/bash

package="zip"

if yum list installed "$package" >/dev/null 2>&1; then
  echo "$package is already installed"
else
  echo "Installing $package"
  yum install -y "$package"
fi

#Install eksctl

echo "Install eksctl"
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp

sudo mv /tmp/eksctl /usr/local/bin

#Install kubectl
echo "Install kubectl"
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.24.7/2022-10-31/bin/linux/amd64/kubectl
chmod +x ./kubectl
mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$PATH:$HOME/bin
echo 'export PATH=$PATH:$HOME/bin' >> ~/.bashrc

#Install awscli
echo "Install awscli"
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

#Install Helm
echo "Install Helm"
curl https://get.helm.sh/helm-v3.5.4-linux-amd64.tar.gz -o helm.tar.gz
tar -zxvf helm.tar.gz
sudo mv linux-amd64/helm /usr/local/bin/

#Verify Helm Installation
echo "Verifying Helm Installation"
helm version
