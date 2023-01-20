# A couple of simple scripts to access ec2 using ssm

# instance-status.sh
Script will lists instances based on instance id with tag Name 

# instance-connect.sh
This script will use session manager to access an instance

# Note
You will need to create an IAM profile to use these scripts 

```
aws configure --profile website-account
```

I would suggest creating an alias in bashrc or bash_profile