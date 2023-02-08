import boto3

class Ec2List:
    def __init__(self):

        self.client = boto3.client('ec2')
        self.response = self.client.describe_instances

    def ec2_list(self):
        list = self.response(Filters=[{
            'Name': 'tag:Name',
            'Values': ['*']
            }]
        )

        for reservation in list['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']

                instance_name = None
                for tag in instance.get('Tags', []):
                    if tag['Key'] == 'Name':
                        instance_name = tag['Value']
                        break

                if instance_name:
                    print(f'Instance ID: {instance_id} - Name: {instance_name}')

                else:
                    print(f'Instance ID: {instance_id} - No Name tag found')
    
ec2_object = Ec2List()
ec2_object.ec2_list()
