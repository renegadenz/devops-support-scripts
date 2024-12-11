#!/bin/bash

# Export region dynamically from AWS CLI
export REGION=$(aws configure get region)

# List of required endpoints
REQUIRED_ENDPOINTS=(
    "com.amazonaws.${REGION}.s3"
    "com.amazonaws.${REGION}.monitoring"
    "com.amazonaws.${REGION}.logs"
    "com.amazonaws.${REGION}.sqs"
    "com.amazonaws.${REGION}.kms"
)

# Function to check VPC Endpoint Status
check_endpoint_status() {
    echo -e "\nChecking VPC Endpoint Status..."

    # Describe VPC endpoints using AWS CLI
    ENDPOINTS=$(aws ec2 describe-vpc-endpoints --query "VpcEndpoints[].ServiceName" --output text)

    for endpoint in "${REQUIRED_ENDPOINTS[@]}"; do
        if echo "$ENDPOINTS" | grep -q "$endpoint"; then
            STATE=$(aws ec2 describe-vpc-endpoints --filters "Name=service-name,Values=$endpoint" --query "VpcEndpoints[0].State" --output text)
            echo "Endpoint $endpoint: $STATE"
            if [ "$STATE" != "available" ]; then
                echo "⚠️ Endpoint $endpoint is not available!"
            fi
        else
            echo "❌ Endpoint $endpoint is missing!"
        fi
    done
}

# Function to check DNS resolution
check_dns_resolution() {
    local endpoint=$1
    echo "Resolving DNS for $endpoint..."

    # Resolve DNS for the endpoint
    IP=$(dig +short $endpoint)

    if [ -n "$IP" ]; then
        echo "✅ Resolved $endpoint to IP: $IP"
        return 0
    else
        echo "❌ DNS resolution failed for $endpoint"
        return 1
    fi
}

# Function to test connectivity
test_connectivity() {
    local endpoint=$1
    echo "Testing connectivity to $endpoint..."

    # Test connectivity using curl
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://$endpoint")

    if [ "$HTTP_STATUS" == "200" ]; then
        echo "✅ Connectivity to $endpoint successful!"
    else
        echo "❌ Connectivity to $endpoint failed with status code: $HTTP_STATUS"
    fi
}

# Main function
main() {
    # Validate VPC Endpoint Status
    check_endpoint_status

    # Validate DNS and Connectivity
    echo -e "\nValidating DNS and Connectivity..."
    for service in "${REQUIRED_ENDPOINTS[@]}"; do
        # Convert service name to endpoint DNS
        SERVICE_ENDPOINT="${service#com.amazonaws.}"
        SERVICE_ENDPOINT="${SERVICE_ENDPOINT//./-}.amazonaws.com"

        if check_dns_resolution "$SERVICE_ENDPOINT"; then
            test_connectivity "$SERVICE_ENDPOINT"
        fi
    done
}

# Run the main function
main
