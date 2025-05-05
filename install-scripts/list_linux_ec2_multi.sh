#!/bin/bash

# Ensure at least one profile is passed
if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <aws_profile_1> [<aws_profile_2> ...]"
  exit 1
fi

for PROFILE in "$@"; do
  echo ""
  echo "=============================================="
  echo "Profile: $PROFILE"
  echo "=============================================="

  # Get all AWS regions for the current profile
  REGIONS=$(aws ec2 describe-regions --query 'Regions[*].RegionName' --output text --profile "$PROFILE" 2>/dev/null)

  if [ $? -ne 0 ]; then
    echo "Error: Unable to fetch regions with profile $PROFILE"
    continue
  fi

  for REGION in $REGIONS; do
    echo ""
    echo "Region: $REGION"
    echo "------------------------------"

    aws ec2 describe-instances \
      --profile "$PROFILE" \
      --region "$REGION" \
      --query 'Reservations[*].Instances[?PlatformDetails==`Linux/UNIX`].[InstanceId,InstanceType,State.Name,PrivateIpAddress,Tags[?Key==`Name`]|[0].Value]' \
      --output table \
      --no-paginate 2>/dev/null
  done
done
