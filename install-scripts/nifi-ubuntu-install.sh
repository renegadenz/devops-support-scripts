#!/bin/bash

# Update the system
sudo apt update && sudo apt upgrade -y

# Check if Java 11 is installed, if not install it
if ! java -version 2>&1 | grep -q "version \"11"
then
    sudo apt install -y openjdk-11-jdk
fi

# Check if unzip is installed, if not install it
if ! unzip -v &> /dev/null
then
    sudo apt install -y unzip
fi

# Download Apache NiFi if it's not already downloaded
if [ ! -f "nifi-1.22.0-bin.zip" ]
then
    wget https://downloads.apache.org/nifi/1.22.0/nifi-1.22.0-bin.zip
fi

# Extract the downloaded package
unzip -q nifi-1.22.0-bin.zip

# Move NiFi to the desired location if it's not already there
if [ ! -d "/opt/nifi" ]
then
    sudo mv nifi-1.22.0 /opt/nifi
fi

# Create a new system user for NiFi if it doesn't exist already
if ! id -u nifi &> /dev/null
then
    sudo useradd -r -s /bin/false nifi
fi

# Change the ownership of the NiFi directory to the nifi user
sudo chown -R nifi:nifi /opt/nifi

# Set up NiFi environment variables
if ! grep -q "NIFI_HOME" ~/.bashrc
then
    echo 'export NIFI_HOME="/opt/nifi"' >> ~/.bashrc
    echo 'export PATH="$NIFI_HOME/bin:$PATH"' >> ~/.bashrc
fi

# Explicitly set the environment variables within the script
export NIFI_HOME="/opt/nifi"
export PATH="$NIFI_HOME/bin:$PATH"

# Create a directory for the logs and make nifi the owner
sudo mkdir -p /var/log/nifi
sudo chown nifi:nifi /var/log/nifi

# Remove existing logs directory in NiFi
sudo rm -rf $NIFI_HOME/logs

# Create a symbolic link from the NiFi logs directory to /var/log/nifi
sudo ln -s /var/log/nifi $NIFI_HOME/logs

# Uncomment the following line to increase the maximum heap size (optional)
# sudo sed -i 's/nifi.app.heap.size=512m/nifi.app.heap.size=2g/' $NIFI_HOME/conf/nifi.properties

# Modify nifi.properties to disable SSL and enable HTTP
sudo sed -i 's/nifi.remote.input.secure=.*/nifi.remote.input.secure=false/' $NIFI_HOME/conf/nifi.properties
sudo sed -i 's/nifi.web.http.host=.*/nifi.web.http.host=0.0.0.0/' $NIFI_HOME/conf/nifi.properties
sudo sed -i 's/nifi.web.http.port=.*/nifi.web.http.port=8080/' $NIFI_HOME/conf/nifi.properties
sudo sed -i 's/nifi.web.https.host=.*/nifi.web.https.host=/' $NIFI_HOME/conf/nifi.properties
sudo sed -i 's/nifi.web.https.port=.*/nifi.web.https.port=/' $NIFI_HOME/conf/nifi.properties

# Create a systemd service file for NiFi
echo "[Unit]
Description=Apache NiFi service
After=network.target

[Service]
Type=simple
User=nifi
Group=nifi
Environment=\"JAVA_HOME=$(readlink -f /usr/bin/java | sed 's:bin/java::')\"
Environment=\"NIFI_HOME=$NIFI_HOME\"
ExecStart=$NIFI_HOME/bin/nifi.sh run
ExecStop=$NIFI_HOME/bin/nifi.sh stop
Restart=on-failure

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/nifi.service > /dev/null

# Reload systemd daemon to recognize changes
sudo systemctl daemon-reload

# Enable the NiFi service
sudo systemctl enable nifi.service

# Start NiFi if it's not already running
if ! systemctl is-active --quiet nifi.service
then
    sudo systemctl start nifi.service
fi
