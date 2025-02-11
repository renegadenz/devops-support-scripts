import boto3
import csv
import os
import configparser

def get_aws_profiles():
    """Retrieve AWS profile names from credentials and config files."""
    profiles = set()
    aws_dir = os.path.expanduser("~/.aws")
    
    for file_name in ["credentials", "config"]:
        file_path = os.path.join(aws_dir, file_name)
        if os.path.exists(file_path):
            config = configparser.ConfigParser()
            config.read(file_path)
            for section in config.sections():
                if section.startswith("profile "):  # Config file format
                    profiles.add(section.split("profile ")[1])
                else:  # Credentials file format
                    profiles.add(section)

    return sorted(profiles)

def get_hosted_zones(profile):
    """Retrieve hosted zones for the selected AWS profile."""
    session = boto3.Session(profile_name=profile)
    client = session.client("route53")
    
    hosted_zones = client.list_hosted_zones()["HostedZones"]
    return [(zone["Id"].split("/")[-1], zone["Name"]) for zone in hosted_zones]

def get_dns_records(profile, zone_id):
    """Retrieve all DNS records for a specific hosted zone."""
    session = boto3.Session(profile_name=profile)
    client = session.client("route53")

    records = []
    paginator = client.get_paginator("list_resource_record_sets")
    for page in paginator.paginate(HostedZoneId=zone_id):
        records.extend(page["ResourceRecordSets"])

    return records

def export_to_csv(records, zone_name):
    """Export DNS records to a CSV file."""
    filename = f"{zone_name.strip('.')}_dns_records.csv"
    
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Type", "TTL", "Value"])
        
        for record in records:
            name = record.get("Name", "")
            rtype = record.get("Type", "")
            ttl = record.get("TTL", "N/A")
            values = [r["Value"] for r in record.get("ResourceRecords", [])]
            
            writer.writerow([name, rtype, ttl, ", ".join(values)])

    print(f"DNS records exported to {filename}")

def main():
    # Step 1: List and select AWS profile
    profiles = get_aws_profiles()
    if not profiles:
        print("No AWS profiles found. Ensure your AWS CLI is configured.")
        return

    print("\nAvailable AWS Profiles:")
    for i, profile in enumerate(profiles, 1):
        print(f"{i}. {profile}")

    profile_index = int(input("\nSelect AWS Profile (number): ")) - 1
    profile = profiles[profile_index]

    # Step 2: List and select hosted zones
    zones = get_hosted_zones(profile)
    if not zones:
        print("No hosted zones found.")
        return

    print("\nAvailable Hosted Zones:")
    for i, (zone_id, zone_name) in enumerate(zones, 1):
        print(f"{i}. {zone_name} ({zone_id})")

    zone_index = int(input("\nSelect Hosted Zone (number): ")) - 1
    zone_id, zone_name = zones[zone_index]

    # Step 3: Get DNS records and export to CSV
    records = get_dns_records(profile, zone_id)
    if not records:
        print("No DNS records found.")
    else:
        export_to_csv(records, zone_name)

if __name__ == "__main__":
    main()
