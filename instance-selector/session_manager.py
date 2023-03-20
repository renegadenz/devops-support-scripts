#!/usr/bin/env python3

import argparse
import boto3
import subprocess

def create_session(profile_name=None, region_name=None):
    session = boto3.Session(profile_name=profile_name, region_name=region_name)
    return session

def get_active_ec2_instances(session):
    ec2 = session.resource('ec2')
    instances = ec2.instances.filter(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['running', 'pending']}
        ]
    )
    return instances

def get_instance_name(instance):
    name_tag = [tag['Value'] for tag in instance.tags if tag['Key'] == 'Name']
    return name_tag[0] if name_tag else 'N/A'

def display_active_instances(instances):
    print("Active EC2 instances:")
    for index, instance in enumerate(instances, start=1):
        name = get_instance_name(instance)
        print(f"{index}. ID: {instance.id}, Name: {name}, Type: {instance.instance_type}, State: {instance.state['Name']}, Launch Time: {instance.launch_time}")

def parse_args():
    parser = argparse.ArgumentParser(description="Get active EC2 instances for a specific AWS profile and region.")
    parser.add_argument('--profile', help='The AWS profile to use', default=None)
    parser.add_argument('--region', help='The AWS region to use', default=None)
    return parser.parse_args()

def start_session_manager(instance_id, profile_name=None, region_name=None):
    profile_option = f"--profile {profile_name}" if profile_name else ""
    region_option = f"--region {region_name}" if region_name else ""
    subprocess.run(f"aws ssm start-session --target {instance_id} {profile_option} {region_option}", shell=True, check=True)

if __name__ == "__main__":
    args = parse_args()
    session = create_session(profile_name=args.profile, region_name=args.region)
    active_instances = list(get_active_ec2_instances(session))
    display_active_instances(active_instances)

    if active_instances:
        selected_instance = None
        while not selected_instance:
            try:
                choice = int(input("Enter the number of the instance you want to connect to: "))
                if 1 <= choice <= len(active_instances):
                    selected_instance = active_instances[choice - 1]
                else:
                    print("Invalid choice. Please select a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        print(f"Starting Session Manager for instance {selected_instance.id}...")
        start_session_manager(selected_instance.id, profile_name=args.profile, region_name=args.region)
    else:
        print("No active instances found.")
