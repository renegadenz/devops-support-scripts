import boto3
import sys

AWS_REGION = "ap-southeast-2"  # Pre-set AWS region

def list_instances(ec2_client):
    """Retrieve and display all instances with their IDs, names, and IMDSv2 status."""
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

            # Get IMDSv2 status
            metadata_options = instance.get('MetadataOptions', {})
            imds_status = metadata_options.get('HttpTokens', 'unknown')

            instances.append((instance_id, name, state, imds_status))
    
    if not instances:
        print("No EC2 instances found in the region.")
        sys.exit(1)

    print(f"\n🔹 EC2 Instances in {AWS_REGION}:")
    print(f"{'No.':<5} {'Instance ID':<20} {'Name':<30} {'State':<10} {'IMDSv2':<10}")
    print("-" * 80)

    for i, (instance_id, name, state, imds_status) in enumerate(instances, start=1):
        print(f"{i:<5} {instance_id:<20} {name:<30} {state:<10} {imds_status:<10}")

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
    print(f"\n🔹 Using profile: {profile} in region {AWS_REGION}")

    # Create session with selected profile and fixed region
    session = boto3.Session(profile_name=profile, region_name=AWS_REGION)
    ec2_client = session.client('ec2')

    while True:
        # List instances
        instances = list_instances(ec2_client)

        print("\nSelect an instance to modify IMDSv2 settings:")
        print("🔹 Enter the instance number to toggle IMDSv2.")
        print("🔹 Type 'r' to refresh the list.")
        print("🔹 Type 'q' to quit.\n")

        choice = input("Your selection: ").strip().lower()

        if choice == 'q':
            print("Exiting...")
            break
        elif choice == 'r':
            continue
        elif choice.isdigit():
            instance_index = int(choice) - 1
            if instance_index not in range(len(instances)):
                print("Invalid selection.")
                continue

            instance_id, name, state, imds_status = instances[instance_index]
            print(f"\n🔹 Selected Instance: {instance_id} ({name})")

            if imds_status == 'required':
                print(f"✅ IMDSv2 is already enabled on {instance_id}.")
            else:
                confirm = input(f"⚠️ IMDSv2 is NOT enforced on {instance_id}. Apply now? (y/n): ").strip().lower()
                if confirm == 'y':
                    modify_metadata_options(ec2_client, instance_id)
                else:
                    print("Skipped.")
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
