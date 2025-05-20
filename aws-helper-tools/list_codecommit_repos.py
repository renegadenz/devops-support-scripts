# list_codecommit_repos.py
import boto3
import argparse

def list_codecommit_repositories(profile, region):
    session = boto3.Session(profile_name=profile, region_name=region)
    client = session.client('codecommit')

    repos = []
    paginator = client.get_paginator('list_repositories')
    for page in paginator.paginate():
        repos.extend(page['repositories'])

    print("CodeCommit Repositories:")
    for repo in repos:
        print(f"- {repo['repositoryName']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True, help="AWS CLI profile name")
    parser.add_argument("--region", default="ap-southeast-2", help="AWS region")
    args = parser.parse_args()

    list_codecommit_repositories(args.profile, args.region)
