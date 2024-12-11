import boto3
import socket
import subprocess

# AWS Session
session = boto3.Session()
ec2_client = session.client("ec2")
region = session.region_name

# List of required endpoints
REQUIRED_ENDPOINTS = [
    f"com.amazonaws.{region}.s3",
    f"com.amazonaws.{region}.monitoring",
    f"com.amazonaws.{region}.logs",
    f"com.amazonaws.{region}.sqs",
    f"com.amazonaws.{region}.kms",
]

def check_endpoint_status():
    print("\nChecking VPC Endpoint Status...")
    response = ec2_client.describe_vpc_endpoints()
    endpoint_status = {ep['ServiceName']: ep['State'] for ep in response['VpcEndpoints']}
    
    for endpoint in REQUIRED_ENDPOINTS:
        if endpoint in endpoint_status:
            status = endpoint_status[endpoint]
            print(f"Endpoint {endpoint}: {status}")
            if status != "available":
                print(f"⚠️ Endpoint {endpoint} is not available!")
        else:
            print(f"❌ Endpoint {endpoint} is missing!")

def check_dns_resolution(endpoint):
    try:
        print(f"Resolving DNS for {endpoint}...")
        ip = socket.gethostbyname(endpoint)
        print(f"✅ Resolved {endpoint} to IP: {ip}")
        return True
    except socket.gaierror:
        print(f"❌ DNS resolution failed for {endpoint}")
        return False

def test_connectivity(endpoint):
    print(f"Testing connectivity to {endpoint}...")
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", f"https://{endpoint}"],
            capture_output=True,
            text=True
        )
        if result.stdout == "200":
            print(f"✅ Connectivity to {endpoint} successful!")
        else:
            print(f"❌ Connectivity to {endpoint} failed with status code: {result.stdout}")
    except Exception as e:
        print(f"❌ Error testing connectivity: {str(e)}")

def main():
    # Validate VPC Endpoint Status
    check_endpoint_status()
    
    # Validate DNS and Connectivity
    print("\nValidating DNS and Connectivity...")
    for service in REQUIRED_ENDPOINTS:
        # Convert service name to endpoint DNS
        service_endpoint = service.split(".")[1] + f".{region}.amazonaws.com"
        if check_dns_resolution(service_endpoint):
            test_connectivity(service_endpoint)

if __name__ == "__main__":
    main()
