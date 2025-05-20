import boto3
import argparse
import csv
import tempfile
import os

def list_codecommit_repositories(profile, region):
    session = boto3.Session(profile_name=profile, region_name=region)
    client = session.client('codecommit')

    repos = []
    paginator = client.get_paginator('list_repositories')
    for page in paginator.paginate():
        repos.extend(page['repositories'])

    with tempfile.NamedTemporaryFile(mode='w', newline='', suffix='.csv', delete=False, prefix='codecommit_', dir=tempfile.gettempdir()) as temp_file:
        writer = csv.DictWriter(temp_file, fieldnames=["repositoryName", "repositoryId"])
        writer.writeheader()
        writer.writerows(repos)
        print(f"Saved {len(repos)} repositories to {temp_file.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True, help="AWS CLI profile name")
    parser.add_argument("--region", default="ap-southeast-2", help="AWS region")
    args =
