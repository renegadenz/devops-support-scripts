# AWS Lambda function for detecting cost anomalies and sending alerts to Microsoft Teams

This is an AWS Lambda function that uses the AWS SDK for Python to detect cost anomalies in AWS and send alerts to a Microsoft Teams webhook. The function is triggered on a daily schedule and checks the cost and usage data for the current month. If any cost anomalies are detected (i.e. costs that exceed a certain threshold), a message is sent to the specified Microsoft Teams webhook with details of the anomalies.

## Prerequisites
An AWS account
AWS CLI installed and configured
SAM CLI installed
Python 3.8 or later installed
Installation
Clone this repository to your local development environment:

```
git clone https://github.com/renegadenz/devops-support-scripts.git
cd devops-support-scripts/cost-explorer
```
Modify the template.yaml file:

Set the WebhookUrl parameter to the URL of your Microsoft Teams webhook
Adjust the Threshold environment variable to your desired cost anomaly threshold
Build and deploy the Lambda function:

```
sam build
sam deploy --guided
```
Follow the prompts to configure the deployment:

Stack Name: The name of the CloudFormation stack to create/update
AWS Region: The AWS region to deploy the stack to
Parameter WebhookUrl: The URL of your Microsoft Teams webhook
The SAM CLI will package and upload your Lambda function code, create a CloudFormation stack, and deploy the function.

Usage
The Lambda function runs on a daily schedule and checks the cost and usage data for the current month. If any cost anomalies are detected (i.e. costs that exceed the specified threshold), a message is sent to the specified Microsoft Teams webhook with details of the anomalies.

To view the CloudFormation stack in the AWS Management Console, navigate to the CloudFormation service and select the stack that you created. You can view the status of the stack, as well as the resources that were created.

To view the logs for the Lambda function, navigate to the CloudWatch Logs service and select the log group for the function. You can view the logs for each execution of the function.

Cleanup
To delete the CloudFormation stack and the resources that were created, run the following command:

```
aws cloudformation delete-stack --stack-name <stack-name>
```
Replace <stack-name> with the name of the stack that you created.