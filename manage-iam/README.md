# IAM Access Key Rotation Script
This script can be used to rotate the access keys for an IAM user on a local machine. The script uses the AWS CLI to create a new access key, disable the old access key, and print the information for the new access key.

## Requirements
Before using this script, you'll need to have the following:

An AWS account with the appropriate permissions to manage IAM users and access keys.
The AWS CLI installed and configured on your local machine with the appropriate IAM user credentials.

## Usage
To use this script, follow these steps:

Copy the script to a file named rotate-iam-keys.sh on your local machine.
Modify the script as necessary to set the path to the AWS CLI executable and the IAM user whose access keys you want to rotate.
Make the script executable by running the following command: chmod +x rotate-iam-keys.sh.
Test the script by running it manually: ./rotate-iam-keys.sh. Verify that it creates a new access key, disables the old access key, and prints the information for the new access key.
Set up a cron job to run the script automatically. For example, to run the script every three months, you can use the following cron expression: 
```
0 0 1 */3 * /path/to/rotate-iam-keys.sh.
```
Make sure to replace /path/to with the actual path to the script on your local machine.
Note that this script rotates the access keys for a single IAM user. If you need to rotate the access keys for multiple users, you'll need to modify the script or create separate scripts for each user.

I hope this helps you to use the IAM access key rotation script. If you have any questions or need further assistance, feel free to reach out.
