# IAM Access Key Remover
This repository contains a SAM template and a Python Lambda function to remove inactive IAM user access keys older than 7 days and send notifications via SNS. The Lambda function is triggered once a day at 12:00 PM (UTC) by EventBridge.

## Prerequisites
AWS CLI - Make sure to configure it with your AWS credentials.
AWS SAM CLI - Install the AWS SAM CLI to package and deploy the application.

## Deployment
Follow the steps below to deploy the IAM Access Key Remover using the AWS SAM CLI:

Clone this repository:

```
git clone https://github.com/renegadenz/devops-support-scripts.git
cd devops-support-scripts/inactive-access-key-removal-lambda
```
2. Package the application:

```
sam package --template-file inactive-access-key-removal.yaml --s3-bucket your-s3-bucket --output-template-file packaged-template.yaml
```
Replace your-s3-bucket with an existing S3 bucket in your AWS account where the deployment artifacts will be uploaded. If you have used CloudFormation before in the account, you probably find a default bucket cf-templates-<id>-<region>.

3. Deploy the application:
```
sam deploy --template-file packaged-template.yaml --stack-name inactive-access-key-remover --capabilities CAPABILITY_IAM --parameter-overrides "IAMUserNames=user1,user2,user3"
```
Replace user1,user2,user3 with a comma-separated list of IAM user names whose inactive access keys should be removed.

The deployment process will create a CloudFormation stack containing the Lambda function, EventBridge rules, and the SNS topic. You can monitor the progress of the deployment in the AWS CloudFormation console.

Updating the Application

If you make changes to the Lambda function or the SAM template and want to update the deployed application, follow these steps:

1. Package the updated application:

```
sam package --template-file inactive-access-key-removal.yaml --s3-bucket your-s3-bucket --output-template-file packaged-template.yaml
```

2. Deploy the updated application:
```
sam deploy --template-file packaged-template.yaml --stack-name inactive-access-key-remover --capabilities CAPABILITY_IAM --parameter-overrides "IAMUserNames=user1,user2,user3"
```
The CloudFormation stack will be updated with the changes. Check the AWS CloudFormation console for the update progress.

3. Cleaning Up
To delete the resources created by the IAM Access Key Remover, run the following command:
```
aws cloudformation delete-stack --stack-name inactive-access-key-remover
```
This will remove the Lambda function, EventBridge rules, and associated resources. Note that any S3 objects created during the packaging process will need to be deleted manually.