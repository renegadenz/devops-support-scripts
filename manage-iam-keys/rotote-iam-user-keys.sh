#!/bin/bash

# Set the path to the AWS CLI executable
AWS_CLI="/usr/local/bin/aws"

# Set the IAM user whose access keys you want to rotate
IAM_USER="my-iam-user"

# Get the list of access keys for the IAM user
ACCESS_KEYS=$($AWS_CLI iam list-access-keys --user-name "$IAM_USER" --query 'AccessKeyMetadata[*].AccessKeyId' --output text)

# Loop through the access keys and rotate each one
for ACCESS_KEY in $ACCESS_KEYS; do
  # Create a new access key
  NEW_KEY=$($AWS_CLI iam create-access-key --user-name "$IAM_USER" --query 'AccessKey.{AccessKeyId:AccessKeyId,SecretAccessKey:SecretAccessKey}' --output json)

  # Disable the old access key
  $AWS_CLI iam update-access-key --access-key-id "$ACCESS_KEY" --status Inactive --user-name "$IAM_USER"

  # Print the new access key information
  echo "Created new access key:"
  echo "AccessKeyId: $(echo $NEW_KEY | jq -r '.AccessKeyId')"
  echo "SecretAccessKey: $(echo $NEW_KEY | jq -r '.SecretAccessKey')"
  echo ""

  # Update the default profile with the new access key
  $AWS_CLI configure set aws_access_key_id "$(echo $NEW_KEY | jq -r '.AccessKeyId')" --profile default
  $AWS_CLI configure set aws_secret_access_key "$(echo $NEW_KEY | jq -r '.SecretAccessKey')" --profile default

  # Exit after updating the default profile with the first new access key
  break
done
