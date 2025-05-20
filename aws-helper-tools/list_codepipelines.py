import boto3
import argparse
import csv
import tempfile

def list_code_pipelines(profile, region):
    session = boto3.Session(profile_name=profile, region_name=region)
    client = session.client('codepipeline')

    pipelines = []
    paginator = client.get_paginator('list_pipelines')
    for page in paginator.paginate():
        pipelines.extend(page['pipelines'])

    fieldnames = ["name", "version", "created", "updated", "pipelineType", "executionMode"]

    with tempfile.NamedTemporaryFile(mode='w', newline='', suffix='.csv', delete=False, prefix='codepipeline_', dir=tempfile.gettempdir()) as temp_file:
        writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
        writer.writeheader()

        for pipeline in pipelines:
            filtered = {k: pipeline.get(k, "") for k in fieldnames}
            writer.writerow(filtered)

        print(f"Saved {len(pipelines)} pipelines to {temp_file.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True, help="AWS CLI profile name")
    parser.add_argument("--region", default="ap-southeast-2", help="AWS region")
    args = parser.parse_args()

    list_code_pipelines(args.profile, args.region)
