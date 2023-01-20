#!/bin/bash

echo "Which AWS Profile?"
read profile
aws ec2 describe-instances \
--query "Reservations[*].Instances[*].{Instance:InstanceId,Type:InstanceType,Name:Tags[?Key=='Name']|[0].Value,Status:State.Name}" --profile $profile \
--output table 
