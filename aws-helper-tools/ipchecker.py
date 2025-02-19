import csv
import os
import time
import pandas as pd
from ipwhois import IPWhois

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

def process_csv_files_in_directory(directory):
    """Process all CSV files in a given directory."""
    unique_ips = set()

    # Loop through all CSV files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            print(f"Processing {file_path}...")
            with open(file_path, "r") as file:
                reader = csv.reader(file, delimiter="\t")
                for row in reader:
                    if len(row) >= 5:
                        external_ip = row[3]  # Assuming column 3 has external IPs
                        unique_ips.add(external_ip)

    # Perform WHOIS lookup for each unique IP
    results = []
    for ip in unique_ips:
        print(f"Checking WHOIS for {ip}...")
        results.append(get_whois_info(ip))
        time.sleep(1)  # Sleep to avoid rate limiting

    # Save results to a CSV file
    df = pd.DataFrame(results)
    output_file = os.path.join(directory, "whois_results.csv")
    df.to_csv(output_file, index=False)
    print(f"WHOIS lookup completed. Results saved to {output_file}.")
    return output_file

# Example usage:
# process_csv_files_in_directory("/path/to/your/directory")
