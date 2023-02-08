import boto3

class Ec2List:
    def __init__(self):
        # Initialize the EC2 client
        self.client = boto3.client('ec2')

    def get_instances(self):
        # Use the EC2 client to get a list of all instances that have a Name tag
        response = self.client.describe_instances(
            Filters=[{
                'Name': 'tag:Name',
                'Values': ['*']
            }]
        )
        return response['Reservations']

    def print_instance_info(self, instance):
        # Print the instance ID, Name (if present), and state of a single instance
        instance_id = instance['InstanceId']
        instance_name = self.get_instance_name(instance)
        instance_state = instance.get('State', {}).get('Name', 'Unknown')

        if instance_name:
            print(f'Instance ID: {instance_id} - Name: {instance_name} - Instance State: {instance_state}' )
        else:
            print(f'Instance ID: {instance_id} - No Name tag found - Instance State: {instance_state}')

    def get_instance_name(self, instance):
        # Extract the Name tag of a single instance
        for tag in instance.get('Tags', []):
            if tag['Key'] == 'Name':
                return tag['Value']
        return None

    def ec2_list(self):
        # Get the list of all instances and print the information for each running instance
        reservations = self.get_instances()
        for reservation in reservations:
            for instance in reservation['Instances']:
                instance_state = instance.get('State', {}).get('Name', 'Unknown')
                if instance_state != 'running':
                    continue
                self.print_instance_info(instance)

# Create an instance of the Ec2List class
ec2_object = Ec2List()
# Call the ec2_list method to print the information for all running instances
ec2_object.ec2_list()
