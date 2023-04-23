#!/bin/bash

# Define directory for binaries
bin_dir="/usr/local/bin"

# Install zip package if not installed
package="zip"

if dpkg -s "$package" >/dev/null 2>&1; then
  echo "$package is already installed"
else
  echo "Installing $package"
  sudo apt-get update
  sudo apt-get install -y "$package"
fi

# Install eksctl
echo "Installing eksctl"
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl "$bin_dir"

# Install kubectl
echo "Installing kubectl"
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x ./kubectl
sudo mv ./kubectl "$bin_dir"

# Install awscli
echo "Installing awscli"
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install --install-dir "$bin_dir"

# Install Helm
echo "Installing Helm"
curl https://get.helm.sh/helm-v3.5.4-linux-amd64.tar.gz -o helm.tar.gz
tar -zxvf helm.tar.gz
sudo mv linux-amd64/helm "$bin_dir"

# Verify Helm installation
echo "Verifying Helm installation"
helm version

# Clean up downloaded files
echo "Cleaning up downloaded files"
rm -f eksctl_$(uname -s)_amd64.tar.gz awscliv2.zip helm.tar.gz
rm -rf aws/ linux-amd64/

