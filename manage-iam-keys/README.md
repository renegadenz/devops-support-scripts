# IAM Access Key Rotation and Cleanup Scripts
These scripts can be used to rotate the access keys for an IAM user on a local machine and clean up deactivated keys. The rotation script uses the AWS CLI to create a new access key, disable the old access key, update the default AWS profile, and print the information for the new access key. The cleanup script removes deactivated access keys for the specified IAM user.

## Requirements
Before using these scripts, you'll need to have the following:

1. An AWS account with the appropriate permissions to manage IAM users and access keys.
2. The AWS CLI installed and configured on your local machine with the appropriate IAM user credentials.
3. The jq command-line JSON processor installed on your local machine.
# Usage
## Access Key Rotation Script
To use the access key rotation script, follow these steps:

1. Copy the script to a file named rotate-iam-keys.sh on your local machine.
2. Modify the script as necessary to set the path to the AWS CLI executable and the IAM user whose access keys you want to rotate.
3. Make the script executable by running the following command: chmod +x rotate-iam-keys.sh.
4. Test the script by running it manually: ./rotate-iam-keys.sh. Verify that it creates a new access key, disables the old access key, updates the default AWS profile, and 5. prints the information for the new access key.
5. Set up a cron job to run the script automatically. For example, to run the script every three months, you can use the following cron expression: 0 0 1 */3 * /path/to/rotate-iam-keys.sh. Make sure to replace /path/to with the actual path to the script on your local machine.

## Access Key Cleanup Script

To use the access key cleanup script, follow these steps:

1. Copy the script to a file named cleanup-deactivated-keys.sh on your local machine.
2. Modify the script as necessary to set the path to the AWS CLI executable and the IAM user whose deactivated access keys you want to remove.
3. Make the script executable by running the following command: chmod +x cleanup-deactivated-keys.sh.
4. Test the script by running it manually: ./cleanup-deactivated-keys.sh. Verify that it removes any deactivated access keys for the specified IAM user.
5. Optionally, set up a cron job to run the script automatically, e.g., once a month, using a cron expression like 0 0 1 * * /path/to/cleanup-deactivated-keys.sh. Make sure to replace /path/to with the actual path to the script on your local machine.
Note that these scripts manage the access keys for a single IAM user. If you need to rotate the access keys or clean up deactivated keys for multiple users, you'll need to modify the scripts or create separate scripts for each user.

I hope this helps you to use the IAM access key rotation and cleanup scripts. If you have any questions or need further assistance, feel free to reach out.