## How to Use:
Save the script as ec2_snapshot_manager.py.

Run the script with the AWS CLI profile name and region:

```
python ec2_snapshot_manager.py my-aws-profile ap-southeast-2
```
The script will:

List all EC2 instances in the specified region.
Allow you to select an instance interactively by its number.
Create snapshots for all EBS volumes attached to the selected instance.
