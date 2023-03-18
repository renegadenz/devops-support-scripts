# Kubernetes Tools Installation Script

This script automates the installation of the following tools on a Linux system:

1. zip
2. eksctl
3. kubectl
4. AWS CLI (awscli)
5. Helm

These tools are commonly used for managing Kubernetes clusters and resources, particularly in an AWS environment.

## Prerequisites

- This script is designed to run on Linux systems with `bash` and `yum` package manager.
- Make sure you have `curl`, `tar`, and `unzip` installed on your system.
- You need to have root access to install some of the tools.

## How to run the script

1. Save the script with the name `install_kubernetes_tools.sh` or any other preferred name.

2. Make the script executable by running the following command:

```bash
chmod +x install_kubernetes_tools.sh
```
3. Run the script with root privileges:
```
sudo ./install_kubernetes_tools.sh
```

The script will install the required tools and display progress messages during the installation process. Once the script has completed, you can verify the installation of each tool by checking their respective version commands.

For example:

eksctl version
kubectl version --client
aws --version
helm version