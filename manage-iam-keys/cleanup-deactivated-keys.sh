#!/bin/bash

# Set the path to the AWS CLI executable
AWS_CLI="/usr/local/bin/aws"

# Set the IAM user whose access keys you want to clean up
IAM_USER="my-iam-user"

# Get the list of deactivated access keys for the IAM user
DEACTIVATED_KEYS=$($AWS_CLI iam list-access-keys --user-name "$IAM_USER" --query "AccessKeyMetadata[?Status=='Inactive'].AccessKeyId" --output text)

# Check if there are any deactivated access keys
if [ -z "$DEACTIVATED_KEYS" ]; then
  echo "No deactivated access keys found for user $IAM_USER."
else
  # Loop through the deactivated access keys and delete each one
  for ACCESS_KEY in $DEACTIVATED_KEYS; do
    $AWS_CLI iam delete-access-key --access-key-id "$ACCESS_KEY" --user-name "$IAM_USER"
    echo "Deleted deactivated access key: $ACCESS_KEY"
  done
fi
