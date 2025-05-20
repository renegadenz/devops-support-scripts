import boto3
import argparse
import csv

def list_codecommit_repositories(profile, region, output_file):
    session = boto3.Session(profile_name=profile, region_name=region)
    client = session.client('codecommit')

    repos = []
    paginator = client.get_paginator('list_repositories')
    for page in paginator.paginate():
        repos.extend(page['repositories'])

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["repositoryName", "repositoryId"])
        writer.writeheader()
        writer.writerows(repos)

    print(f"Saved {len(repos)} repositories to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True, help="AWS CLI profile name")
    parser.add_argument("--region", default="ap-southeast-2", help="AWS region")
    parser.add_argument("--output", default="codecommit_repos.csv", help="Output CSV file name")
    args = parser.parse_args()

    list_codecommit_repositories(args.profile, args.region, args.output)
