#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <tag-value>"
    exit 1
fi

tag_value="$1"
profile="${2:-default}"

instance_names=$(aws ec2 describe-instances --filters "Name=tag-value,Values=$tag_value" --query "Reservations[*].Instances[*].Tags[?Key=='Name'].Value[]" --output text --profile "$profile" | cut -f1 | sort | uniq)

echo "$instance_names"
