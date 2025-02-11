import boto3
import sys
import csv

def list_ec2_instances_using_resource_explorer(region='ap-southeast-2', profile=None):
    """Retrieve EC2 instance details (ID and Name tag) using AWS Resource Explorer."""

    # Initialize AWS session with the selected profile
    try:
        session = boto3.Session(profile_name=profile) if profile else boto3.Session()
        resource_explorer = session.client('resource-explorer-2', region_name=region)
    except Exception as e:
        print(f"Error initializing AWS session: {e}")
        sys.exit(1)

    try:
        response = resource_explorer.search(
            QueryString="service:ec2 ResourceType:ec2:instance",
            MaxResults=50  # Adjust if needed
        )
    except Exception as e:
        print(f"Error querying AWS Resource Explorer: {e}")
        sys.exit(1)

    instances = []
    
    for item in response.get('Resources', []):
        arn = item.get('Arn', 'N/A')
        tags = {t['Key']: t['Value'] for t in item.get('Tags', [])}
        instance_name = tags.get('Name', 'N/A')  # Fetch Name tag if available

        instances.append({
            "Instance ID": arn.split("/")[-1],  # Extract instance ID from ARN
            "Instance Name": instance_name
        })

    # Print results in a structured table format
    print(f"\n{'Instance ID':<20}{'Instance Name':<30}")
    print("=" * 50)
    for instance in instances:
        print(f"{instance['Instance ID']:<20}{instance['Instance Name']:<30}")

    # Ask if user wants to save to CSV
    save_csv = input("\nDo you want to save the results to a CSV file? (yes/no): ").strip().lower()
    if save_csv == "yes":
        filename = input("Enter the CSV file name (default: ec2_instances.csv): ").strip()
        filename = filename if filename else "ec2_instances.csv"

        # Save results to CSV
        with open(filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Instance ID", "Instance Name"])
            writer.writeheader()
            writer.writerows(instances)

        print(f"\n✅ Results saved to {filename}")

if __name__ == "__main__":
    # Prompt for AWS profile selection
    profile = input("Enter AWS profile name (leave blank for default): ").strip()
    list_ec2_instances_using_resource_explorer(profile=profile if profile else None)
