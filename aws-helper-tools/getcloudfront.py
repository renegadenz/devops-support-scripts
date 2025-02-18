import boto3
import csv
import os

# Function to list available AWS profiles
def list_profiles():
    session = boto3.session.Session()
    return session.available_profiles

# Function to get CloudFront distributions
def get_cloudfront_distributions(profile_name):
    # Initialize CloudFront client with the selected profile
    session = boto3.Session(profile_name=profile_name)
    client = session.client("cloudfront")

    distributions = []
    paginator = client.get_paginator("list_distributions")

    for page in paginator.paginate():
        if "DistributionList" in page and "Items" in page["DistributionList"]:
            for dist in page["DistributionList"]["Items"]:
                distributions.append({
                    "Id": dist["Id"],
                    "DomainName": dist["DomainName"],
                    "Aliases": ", ".join(dist.get("Aliases", {}).get("Items", [])) if dist.get("Aliases") else "N/A",
                    "Status": dist["Status"],
                    "Comment": dist.get("Comment", ""),
                    "LastModifiedTime": dist["LastModifiedTime"]
                })

    return distributions

# List available profiles and prompt the user to select one
profiles = list_profiles()

if not profiles:
    print("No AWS profiles found! Please configure them using 'aws configure'.")
    exit(1)

print("\nAvailable AWS Profiles:")
for i, profile in enumerate(profiles, 1):
    print(f"{i}. {profile}")

selected_index = int(input("\nEnter the number of the profile to use: ")) - 1

if selected_index < 0 or selected_index >= len(profiles):
    print("Invalid selection. Exiting.")
    exit(1)

selected_profile = profiles[selected_index]

# Fetch CloudFront distributions using the selected profile
print(f"\nUsing AWS profile: {selected_profile}")
distributions = get_cloudfront_distributions(selected_profile)

# Save to CSV
csv_file = "cloudfront_distributions.csv"
with open(csv_file, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["Id", "DomainName", "Aliases", "Status", "Comment", "LastModifiedTime"])
    writer.writeheader()
    writer.writerows(distributions)

print(f"\nCSV file '{csv_file}' has been created successfully.")
