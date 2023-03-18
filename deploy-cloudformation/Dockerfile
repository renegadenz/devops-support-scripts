# Use the official Python image as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Install the required packages
RUN pip install --no-cache-dir boto3 PyYAML

# Copy the script into the container
COPY deploy-cloudformation.py .

# Set the entrypoint to run the script
ENTRYPOINT ["python", "deploy-cloudformation.py"]
