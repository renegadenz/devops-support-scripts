import boto3
import datetime
import os

def lambda_handler(event, context):
    # Get the names of the IAM users to remove inactive access keys for
    user_names = os.environ['IAM_USER_NAMES'].split(',')

    # Create an IAM client
    iam_client = boto3.client('iam')

    # Loop through the IAM users and remove inactive access keys older than 7 days for each one
    for user_name in user_names:
        # Get the list of access keys for the IAM user
        access_keys = iam_client.list_access_keys(UserName=user_name)['AccessKeyMetadata']

        # Loop through the access keys and remove any that are inactive and older than 7 days
        for access_key in access_keys:
            if access_key['Status'] == 'Inactive':
                age = datetime.datetime.now(datetime.timezone.utc) - access_key['CreateDate']
                if age > datetime.timedelta(days=7):
                    print(f"Removing inactive access key '{access_key['AccessKeyId']}' for user '{user_name}'...")
                    iam_client.delete_access_key(UserName=user_name, AccessKeyId=access_key['AccessKeyId'])

        # Send a notification to the SNS topic
        topic_arn = os.environ['SNS_TOPIC_ARN']
        sns_client = boto3.client('sns')
        message = f"Removed inactive access keys older than 7 days for IAM user '{user_name}'."
        sns_client.publish(TopicArn=topic_arn, Message=message)

        print(f"Removed inactive access keys older than 7 days for user '{user_name}'.")

