import boto3
import datetime
from openpyxl import Workbook

# Set up AWS client
client = boto3.client('savingsplans')

# Define time range (last 30 days)
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=30)

# Fetch savings plan utilisation
response = client.describe_savings_plans_utilization(
    TimePeriod={
        'Start': start_date.strftime('%Y-%m-%d'),
        'End': end_date.strftime('%Y-%m-%d')
    }
)

utilization_data = response.get('SavingsPlansUtilizationsByTime', [])

# Create spreadsheet
wb = Workbook()
ws = wb.active
ws.title = "Savings Plan Utilisation"

# Headers
headers = [
    "Date",
    "Total Commitment (USD)",
    "Used Commitment (USD)",
    "Unused Commitment (USD)",
    "Utilization (%)"
]
ws.append(headers)

# Fill rows
for item in utilization_data:
    date = item['TimePeriod']['Start']
    utilization = item['Utilization']
    
    total_commitment = utilization['TotalCommitmentToDate']
    used_commitment = utilization['UsedCommitmentToDate']
    unused_commitment = utilization['UnusedCommitmentToDate']
    utilization_percent = utilization['UtilizationPercentage']

    ws.append([
        date,
        float(total_commitment),
        float(used_commitment),
        float(unused_commitment),
        float(utilization_percent)
    ])

# Save spreadsheet
output_file = "savings_plan_utilisation.xlsx"
wb.save(output_file)

print(f"Savings Plan utilisation exported to: {output_file}")
