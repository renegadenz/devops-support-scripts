import boto3
import json
import requests

def lambda_handler(event, context):
    # Set up AWS SDK clients
    ce = boto3.client('ce')
    
    # Get the current month
    today = context.date_time
    year = today.year
    month = today.month
    
    # Get the cost and usage data for the current month
    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': f'{year}-{month}-01',
            'End': f'{year}-{month}-{today.day}'
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost']
    )
    
    # Check for any cost anomalies
    anomalies = [group for group in response['ResultsByTime'][0]['Groups'] if group['Metrics']['UnblendedCost']['Amount'] > 1000]
    
    # If there are anomalies, send a message to Microsoft Teams
    if len(anomalies) > 0:
        message = {
            '@type': 'MessageCard',
            '@context': 'http://schema.org/extensions',
            'summary': 'AWS Cost Anomalies',
            'themeColor': '0078D7',
            'sections': [{
                'activityTitle': f'There are {len(anomalies)} cost anomalies in AWS for the current month.',
                'activitySubtitle': 'Threshold: $1000',
                'activityImage': 'https://docs.microsoft.com/en-us/microsoftteams/platform/media/image-placeholder.png',
                'facts': [{'name': anomaly['Keys'][0], 'value': f'${anomaly["Metrics"]["UnblendedCost"]["Amount"]:.2f}'} for anomaly in anomalies]
            }]
        }
        
        webhook_url = 'your-webhook-url'
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(webhook_url, headers=headers, json=message)
        
        if response.status_code != 200:
            raise ValueError(f'Request to Microsoft Teams returned an error: {response.status_code}, {response.text}')
