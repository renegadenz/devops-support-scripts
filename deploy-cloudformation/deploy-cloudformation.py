import boto3
import sys
import yaml
import time

def validate_template(client, template_body):
    try:
        response = client.validate_template(TemplateBody=template_body)
        print("Template validation successful")
        return True
    except Exception as e:
        print(f"Template validation failed: {e}")
        return False

def monitor_stack_creation(client, stack_name):
    print("Monitoring stack creation events...")
    stack_status = "CREATE_IN_PROGRESS"
    seen_events = set()

    while stack_status == "CREATE_IN_PROGRESS":
        events = client.describe_stack_events(StackName=stack_name)["StackEvents"]
        for event in events:
            if event["EventId"] not in seen_events:
                print(f"{event['ResourceStatus']} - {event['ResourceType']} - {event['ResourceStatusReason']}")
                seen_events.add(event["EventId"])

        stack_status = client.describe_stacks(StackName=stack_name)["Stacks"][0]["StackStatus"]
        time.sleep(10)

    return stack_status

def deploy_cloudformation_template(template_file, variables_file, stack_name, region, profile):
    with open(template_file, 'r') as file:
        template_body = file.read()

    with open(variables_file, 'r') as file:
        variables_data = yaml.safe_load(file)

    session = boto3.Session(profile_name=profile, region_name=region)
    client = session.client('cloudformation')

    if not validate_template(client, template_body):
        sys.exit(1)

    try:
        response = client.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=[
                {
                    'ParameterKey': key,
                    'ParameterValue': str(value)
                } for key, value in variables_data.items()
            ],
            Capabilities=[
                'CAPABILITY_IAM',
                'CAPABILITY_NAMED_IAM',
                'CAPABILITY_AUTO_EXPAND'
            ]
        )

        print(f'Stack creation initiated: {response["StackId"]}')
        final_stack_status = monitor_stack_creation(client, stack_name)
        print(f'Stack creation finished with status: {final_stack_status}')

    except Exception as e:
        print(f'Error creating stack: {e}')

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print('Usage: python deploy_cloudformation_template.py <template_file> <variables_file> <stack_name> <region> <profile>')
        sys.exit(1)

    template_file = sys.argv[1]
    variables_file = sys.argv[2]
    stack_name = sys.argv[3]
    region = sys.argv[4]
    profile = sys.argv[5]

    deploy_cloudformation_template(template_file, variables_file, stack_name, region, profile)
