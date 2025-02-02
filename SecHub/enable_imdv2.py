import boto3
import sys

def list_instances(ec2_client):
    """Retrieve and display all instances with their IDs and names."""
    instances = []
    response = ec2_client.describe_instances()
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            name = "N/A"
            for tag in instance.get('Tags', []):
                if tag['Key'] == 'Name':
                    name = tag['Value']
            state = instance['State']['Name']
            instances.append((instance_id, name, state))
    
    if not instances:
        print("No EC2 instances found.")
        sys.exit(1)

    print("\nAvailable EC2 Instances:")
    for i, (instance_id, name, state) in enumerate(instances, start=1):
        print(f"{i}. {instance_id} ({name}) - {state}")
    
    return instances

def modify_metadata_options(ec2_client, instance_id):
    """Enforce IMDSv2 on the given EC2 instance."""
    try:
        ec2_client.modify_instance_metadata_options(
            InstanceId=instance_id,
            HttpTokens='required',
            HttpPutResponseHopLimit=2,
            HttpEndpoint='enabled'
        )
        print(f"\n✅ IMDSv2 enforced successfully on {instance_id}")
    except Exception as e:
        print(f"\n❌ Failed to modify instance metadata options: {e}")

def main():
    """Main script function."""
    import boto3.session

    print("🔹 Available AWS Profiles:")
    session = boto3.Session()
    profiles = session.available_profiles

    if not profiles:
        print("No AWS profiles found. Configure profiles using `aws configure`.")
        sys.exit(1)

    for i, profile in enumerate(profiles, start=1):
        print(f"{i}. {profile}")

    profile_choice = int(input("\nSelect a profile (number): ")) - 1
    if profile_choice not in range(len(profiles)):
        print("Invalid selection.")
        sys.exit(1)

    profile = profiles[profile_choice]
    print(f"\n🔹 Using profile: {profile}")

    # Create session with selected profile
    session = boto3.Session(profile_name=profile)
    ec2_client = session.client('ec2')

    # List and choose instance
    instances = list_instances(ec2_client)
    instance_choice = int(input("\nSelect an instance (number): ")) - 1
    if instance_choice not in range(len(instances)):
        print("Invalid selection.")
        sys.exit(1)

    instance_id = instances[instance_choice][0]
    print(f"\n🔹 Applying IMDSv2 to: {instance_id}")

    # Modify instance metadata options
    modify_metadata_options(ec2_client, instance_id)

if __name__ == "__main__":
    main()
