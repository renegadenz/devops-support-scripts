# Overview
The lambda_function.py script is a Python script that can be deployed as an AWS Lambda function to notify users of AWS access keys that are older than 90 days. The script uses the AWS SDK for Python (boto3) to interact with the AWS Identity and Access Management (IAM) service to check for old access keys and send notifications via Amazon SNS.

## Prerequisites
Before you can deploy the lambda_function.py script, you need to have the following:

* An AWS account (stating the obvious here)
* The AWS CLI (Command Line Interface) installed on your machine
* The AWS SAM CLI (Command Line Interface) installed on your machine
* Basic knowledge of AWS Lambda and AWS SAM

# Deployment

To deploy the lambda_function.py script using AWS SAM, follow these steps:

Clone the repository that contains the script to your local machine.

Navigate to the directory containing the lambda_function.py script in your terminal.

Run the following command to package the lambda function:

```
sam package --template-file access-key-notifier.yaml --s3-bucket your-bucket-name --output-template-file packaged.yaml
```

Replace your-bucket-name with the name of the S3 bucket that you want to use for storing the packaged code. This command will create a new SAM deployment package and upload it to the specified S3 bucket.

If you've used Cloudformation before there is generally a bucket already created 

Run the following command to deploy the lambda function:

```
sam deploy --template-file packaged.yaml --stack-name your-stack-name --capabilities CAPABILITY_IAM
```
Replace your-stack-name with a name for the CloudFormation stack that will be created to deploy the function. This command will create a new CloudFormation stack and deploy the lambda function to your AWS account.

Note: The --capabilities CAPABILITY_IAM option is required to grant AWS CloudFormation permission to create IAM roles.

Once the deployment is complete, the CloudFormation stack will contain the lambda function, the SNS topic, and a CloudWatch Events rule to trigger the lambda function once a day. The SNS topic can be subscribed to by the appropriate users, who will receive a notification via email, SMS, or other supported notification protocol.