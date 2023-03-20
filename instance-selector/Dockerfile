FROM python:3.9-slim

# Install AWS CLI
RUN apt-get update && \
    apt-get install -y curl unzip && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip ./aws

# Install boto3
RUN pip install boto3

# Create a directory for the script
RUN mkdir /app
WORKDIR /app

# Copy the session_manager.py script
COPY session_manager.py /app/session_manager.py

# Set the script as executable
RUN chmod +x /app/session_manager.py

# Set the entrypoint
ENTRYPOINT ["/app/session_manager.py"]
