import boto3
import sys
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def list_instances(ec2):
    try:
        instances = ec2.describe_instances()
        instance_list = []

        print("Available EC2 Instances:")
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                state = instance['State']['Name']
                name_tag = next(
                    (tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'),
                    'No Name'
                )
                print(f"{len(instance_list) + 1}. {instance_id} ({name_tag}) - {state}")
                instance_list.append(instance)

        return instance_list
    except Exception as e:
        print(f"Error listing instances: {e}")
        return []

def create_snapshots(ec2, instance):
    instance_id = instance['InstanceId']
    print(f"Selected Instance: {instance_id}")

    try:
        volumes = instance['BlockDeviceMappings']

        for volume in volumes:
            volume_id = volume['Ebs']['VolumeId']
            print(f"Creating snapshot for volume: {volume_id}")

            response = ec2.create_snapshot(
                VolumeId=volume_id,
                Description=f"Snapshot for volume {volume_id} from instance {instance_id}"
            )

            snapshot_id = response['SnapshotId']
            print(f"Snapshot created: {snapshot_id}")

    except Exception as e:
        print(f"Error creating snapshots for instance {instance_id}: {e}")

def main(profile_name, region):
    try:
        session = boto3.Session(profile_name=profile_name, region_name=region)
        ec2 = session.client('ec2')

        # List and select instance
        instances = list_instances(ec2)
        if not instances:
            print("No instances found in this region.")
            return

        while True:
            try:
                selection = int(input("Select an instance by number (0 to exit): "))
                if selection == 0:
                    print("Exiting...")
                    return
                if 1 <= selection <= len(instances):
                    break
                print(f"Invalid selection. Choose a number between 1 and {len(instances)}.")
            except ValueError:
                print("Please enter a valid number.")

        selected_instance = instances[selection - 1]

        # Create snapshots for the selected instance
        create_snapshots(ec2, selected_instance)

    except NoCredentialsError:
        print("No AWS credentials found. Please configure them.")
    except PartialCredentialsError:
        print("Incomplete AWS credentials found. Please check your setup.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python ec2_snapshot_manager.py <profile-name> <region>")
    else:
        profile_name = sys.argv[1]
        region = sys.argv[2]
        main(profile_name, region)
