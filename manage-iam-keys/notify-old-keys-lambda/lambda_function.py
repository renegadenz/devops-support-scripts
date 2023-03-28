import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    iam = boto3.client('iam')
    sns = boto3.client('sns')
    users = iam.list_users()['Users']
    older_than_90_days = datetime.now() - timedelta(days=90)

    for user in users:
        access_keys = iam.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']
        
        for key in access_keys:
            if key['CreateDate'] < older_than_90_days:
                message = f"Dear {user['UserName']},\n\nYour AWS access key {key['AccessKeyId']} was created on {key['CreateDate']} and is now older than 90 days. Please log in to the AWS Management Console and create a new access key if necessary.\n\nBest regards,\nYour DevOps Team"
                sns.publish(
                    TopicArn='your-topic-arn',
                    Message=message,
                    Subject=f"Old Access Key Notification for {user['UserName']}"
                )
