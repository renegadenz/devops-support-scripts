# AWS Session Manager with EC2 Instance Selector
This document describes how to set up and use a Python script (session_manager.py) that leverages AWS Session Manager to connect to active EC2 instances. The script will display a list of active EC2 instances and allow you to select one to connect to using Session Manager.

## Prerequisites
Install Docker: Follow the instructions for your operating system at Docker's official website.

Install AWS CLI: Follow the instructions at AWS CLI's official website.

Configure AWS CLI: Run aws configure to set up your AWS credentials, default region, and output format.

Ensure you have the necessary AWS credentials and permissions to use EC2 and Session Manager.

Create a Python script named session_manager.py with the provided code.

Create a Dockerfile with the provided configuration.

## Setup
Build the Docker image:

docker build -t session_manager .
Add the following function to your ~/.bash_profile or ~/.bashrc file:

```
function session_manager() {
  docker run -it --rm -v ~/.aws:/root/.aws session_manager --profile "${1:-default}" --region "${2:-us-east-1}"
}
```
Source your ~/.bash_profile or ~/.bashrc file to apply the changes:

```
source ~/.bash_profile
```
Or:
```
source ~/.bashrc
```
## Usage
Run the script with the following command:

```
session_manager your_profile_name your_region_name
```
Replace your_profile_name and your_region_name with the appropriate values for your AWS profile and region. If you don't provide these arguments, the script will use the default profile and region.

The script will display a list of active EC2 instances, including their ID, Name tag, instance type, state, and launch time. You will be prompted to choose an instance by entering its corresponding number.

Upon selecting an instance, the script will start a Session Manager session for the selected instance using the AWS CLI.

Note: The script uses the AWS CLI to start a Session Manager session, which will attempt to open an interactive terminal session within the Docker container. This may not work as expected, since the container environment will be different from your host environment. The primary purpose of this example is to demonstrate how to create a shortcut for running the script using Docker.