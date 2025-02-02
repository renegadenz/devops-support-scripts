import boto3
import csv
import os

# Set AWS profile (Modify as needed)
AWS_PROFILE = "your-profile-name"  # Change this to your AWS profile name
os.environ["AWS_PROFILE"] = AWS_PROFILE

# AWS Region
REGION = "ap-southeast-2"  # Change to your AWS region

# Initialize AWS Clients
securityhub_client = boto3.client("securityhub", region_name=REGION)
ec2_client = boto3.client("ec2", region_name=REGION)

def get_securityhub_findings():
    """Fetch Security Hub findings for EC2 IMDSv2 compliance (EC2.8)."""
    findings = []
    paginator = securityhub_client.get_paginator("get_findings")
    pages = paginator.paginate(
        Filters={
            "Title": [{"Value": "[EC2.8] EC2 instances should use Instance Metadata Service Version 2 (IMDSv2)", "Comparison": "EQUALS"}]
        }
    )
    
    for page in pages:
        for finding in page["Findings"]:
            instance_id = None
            if "Resources" in finding and finding["Resources"]:
                instance_id = finding["Resources"][0]["Id"].split("/")[-1]
            findings.append({
                "FindingId": finding["Id"],
                "InstanceId": instance_id,
                "Status": finding["Compliance"]["Status"],
                "Severity": finding["Severity"]["Label"]
            })
    
    return findings

def get_non_compliant_ec2_instances():
    """Fetch EC2 instances that allow IMDSv1 (not enforcing IMDSv2)."""
    non_compliant_instances = []
    
    response = ec2_client.describe_instances(
        Filters=[{"Name": "metadata-options.http-tokens", "Values": ["optional"]}]
    )

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            non_compliant_instances.append({
                "InstanceId": instance["InstanceId"],
                "HttpTokens": instance["MetadataOptions"]["HttpTokens"]
            })
    
    return non_compliant_instances

def save_to_csv(data, filename):
    """Save the findings and EC2 instances data to a CSV file."""
    if not data:
        print(f"No data to write for {filename}")
        return

    keys = data[0].keys()
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"Results saved to {filename}")

if __name__ == "__main__":
    print(f"Using AWS Profile: {AWS_PROFILE}")

    securityhub_findings = get_securityhub_findings()
    ec2_findings = get_non_compliant_ec2_instances()

    # Save results to CSV
    save_to_csv(securityhub_findings, "securityhub_ec2_imdsv2_findings.csv")
    save_to_csv(ec2_findings, "ec2_non_compliant_instances.csv")

    print("Script execution completed.")
