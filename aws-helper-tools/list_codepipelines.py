# list_codepipelines.py
import boto3
import argparse

def list_code_pipelines(profile, region):
    session = boto3.Session(profile_name=profile, region_name=region)
    client = session.client('codepipeline')

    pipelines = []
    paginator = client.get_paginator('list_pipelines')
    for page in paginator.paginate():
        pipelines.extend(page['pipelines'])

    print("CodePipelines:")
    for pipe in pipelines:
        print(f"- {pipe['name']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True, help="AWS CLI profile name")
    parser.add_argument("--region", default="ap-southeast-2", help="AWS region")
    args = parser.parse_args()

    list_code_pipelines(args.profile, args.region)
