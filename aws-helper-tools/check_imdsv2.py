import boto3
import sys

AWS_REGION = "ap-southeast-2"  # Set your default region

def select_aws_profile():
    """Lists available AWS profiles and allows the user to select one."""
    session = boto3.Session()
    profiles = session.available_profiles

    if not profiles:
        print("❌ No AWS profiles found. Configure profiles using `aws configure`.")
        sys.exit(1)

    print("\n🔹 Available AWS Profiles:")
    for i, profile in enumerate(profiles, start=1):
        print(f"{i}. {profile}")

    try:
        profile_choice = int(input("\nSelect a profile (number): ")) - 1
        if profile_choice not in range(len(profiles)):
            raise ValueError
    except ValueError:
        print("❌ Invalid selection. Please enter a valid number.")
        sys.exit(1)

    return profiles[profile_choice]

def list_instances_imdsv2_status(profile, region=AWS_REGION):
    """Lists EC2 instances and checks if IMDSv2 is enabled."""
    session = boto3.Session(profile_name=profile, region_name=region)
    ec2 = session.client('ec2')

    try:
        response = ec2.describe_instances()
    except Exception as e:
        print(f"❌ Error fetching EC2 instances: {e}")
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
    print(f"\n🔹 Using profile: {profile} in region {region}\n")
    print(f"{'Instance ID':<20}{'Instance Name':<30}{'IMDSv2 Enabled':<15}")
    print("=" * 65)
    for instance in instances:
        print(f"{instance['Instance ID']:<20}{instance['Instance Name']:<30}{instance['IMDSv2 Enabled']:<15}")

if __name__ == "__main__":
    selected_profile = select_aws_profile()
    list_instances_imdsv2_status(selected_profile)
