import csv
import requests
from ipwhois import IPWhois
import time
import pandas as pd

def get_whois_info(ip):
    """Fetch WHOIS information for a given IP address."""
    try:
        obj = IPWhois(ip)
        result = obj.lookup_rdap()
        return {
            "IP": ip,
            "ASN": result.get("asn", "N/A"),
            "ASN_CIDR": result.get("asn_cidr", "N/A"),
            "ASN_COUNTRY": result.get("asn_country_code", "N/A"),
            "ASN_DESCRIPTION": result.get("asn_description", "N/A"),
            "Network Name": result.get("network", {}).get("name", "N/A"),
            "Org": result.get("network", {}).get("org", "N/A"),
            "Country": result.get("network", {}).get("country", "N/A"),
        }
    except Exception as e:
        return {"IP": ip, "Error": str(e)}

def process_csv_and_check_whois(input_file):
    """Process the CSV file, extract IPs, and perform WHOIS lookups."""
    unique_ips = set()
    
    # Read the input file and extract unique external IPs
    with open(input_file, "r") as file:
        reader = csv.reader(file, delimiter="\t")
        for row in reader:
            if len(row) >= 5:
                external_ip = row[3]  # Source IP (external)
                unique_ips.add(external_ip)
    
    # Perform WHOIS lookup for each unique IP
    results = []
    for ip in unique_ips:
        print(f"Checking WHOIS for {ip}...")
        results.append(get_whois_info(ip))
        time.sleep(1)  # Sleep to avoid rate limiting
    
    # Save results to a CSV file
    df = pd.DataFrame(results)
    output_file = "whois_results.csv"
    df.to_csv(output_file, index=False)
    print(f"WHOIS lookup completed. Results saved to {output_file}.")
    return output_file

# Example usage:
# process_csv_and_check_whois("input.csv")
