# Deploy CloudFormation with Variables using Docker
This repository contains a Python script that deploys a CloudFormation template with a separate variables file, and a Dockerfile that allows you to run the script inside a Docker container.

## Prerequisites
Before you begin, you'll need to have the following:

## Docker installed on your system
An AWS account and credentials (access key ID and secret access key) with the appropriate permissions to create CloudFormation stacks
A CloudFormation template file (in YAML or JSON format)
A variables file in YAML format with the parameter values for the CloudFormation stack

## Usage
To use this script, follow these steps:

Clone the devops-support-scripts repository to your local machine:
bash
```
git clone https://github.com/renegadenz/devops-support-scripts.git
```
Change into the deploy-cloudformation subdirectory:

```
cd devops-support-scripts/deploy-cloudformation
```
Build the Docker image by running the following command:
```
docker build -t deploy-cloudformation .
```
Run the deploy-cloudformation container using the following command:

```
docker run -it --rm -v ~/.aws:/root/.aws -v $(pwd):/app/templates deploy-cloudformation <template_file> <variables_file> <stack_name> <region> <profile>
```

Replace <template_file> with the path to your CloudFormation template file, <variables_file> with the path to your YAML file containing the variables, <stack_name> with the desired name for your CloudFormation stack, <region> with the AWS region in which you want to create the stack, and <profile> with the AWS CLI profile you want to use for authentication.

After running the command, the script will create a CloudFormation stack using the specified parameters. The stack creation progress will be displayed in real-time, and the final status of the stack creation process will be printed once the stack creation is completed.
Bash Alias
You can also create a bash alias for the docker run command to make it easier to use. To do this, add the following line to your ~/.bashrc file:

```
alias deploy-cfn='docker run -it --rm -v ~/.aws:/root/.aws -v $(pwd):/app/templates deploy-cloudformation'
```
With this alias set up, you can run the deploy-cloudformation container by typing deploy-cfn followed by the script arguments.
