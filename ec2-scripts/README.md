# List EC2 Instance Names Script

This script uses the AWS CLI to get a list of unique EC2 instance names that match a specific tag value.

## Usage

```
./list_ec2_instance_names.sh <tag-value> [<profile>]
```


- `<tag-value>`: The value of the tag to filter instances by (required).
- `<profile>`: The name of the AWS CLI profile to use (optional, default is "default").

The script outputs a list of unique instance names that have a tag value that matches the specified value.

## Example

```
./list_ec2_instance_names.sh my-tag-value
```

This command will output a list of unique instance names that have a tag value of "my-tag-value".

If you want to specify a different AWS CLI profile, you can do so with the second argument:

```
./list_ec2_instance_names.sh my-tag-value my-profile
```

## Notes

- This script requires the AWS CLI to be installed and configured.
- You must have permission to access the EC2 instances in your AWS account.
- The script outputs only the instance names, not any other information about the instances.
- Instance names are sorted alphabetically and duplicates are removed from the output.
