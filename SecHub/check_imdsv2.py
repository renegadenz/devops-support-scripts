import boto3
import sys

def list_instances_imdsv2_status(region='ap-southeast-2', profile=None):
    # Use specified profile or default if not provided
    session = boto3.Session(profile_name=profile) if profile else boto3.Session()
    ec2 = session.client('ec2', region_name=region)

    try:
        response = ec2.describe_instances()
    except Exception as e:
        print(f"Error fetching EC2 instances: {e}")
        sys.exit(1)

    instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            imds_v2_required = instance.get('MetadataOptions', {}).get('HttpTokens') == 'required'

            # Get the Name tag if it exists
            name_tag = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), 'N/A')

            instances.append({
                "Instance ID": instance_id,
                "Instance Name": name_tag,
                "IMDSv2 Enabled": "Yes" if imds_v2_required else "No"
            })

    # Print results
    print(f"{'Instance ID':<20}{'Instance Name':<30}{'IMDSv2 Enabled':<15}")
    print("=" * 65)
    for instance in instances:
        print(f"{instance['Instance ID']:<20}{instance['Instance Name']:<30}{instance['IMDSv2 Enabled']:<15}")

if __name__ == "__main__":
    profile = input("Enter AWS profile name (leave blank for default): ").strip()
    list_instances_imdsv2_status(profile=profile if profile else None)
