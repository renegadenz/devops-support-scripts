#!/bin/bash

set -e

echo "🔧 Installing unattended-upgrades..."
sudo apt update
sudo apt install -y unattended-upgrades

echo "🔧 Enabling automatic security updates..."
sudo dpkg-reconfigure -f noninteractive unattended-upgrades

echo "🛠️ Configuring automatic reboot after upgrade..."
sudo sed -i 's|//Unattended-Upgrade::Automatic-Reboot "false";|Unattended-Upgrade::Automatic-Reboot "true";|' /etc/apt/apt.conf.d/50unattended-upgrades
sudo sed -i 's|//Unattended-Upgrade::Automatic-Reboot-Time "02:00";|Unattended-Upgrade::Automatic-Reboot-Time "04:30";|' /etc/apt/apt.conf.d/50unattended-upgrades

echo "⏰ Scheduling security updates every Sunday at 4:00 AM via cron..."
# Create a cron job to run 'unattended-upgrade' weekly
CRON_JOB="0 4 * * 0 root /usr/bin/unattended-upgrade -v"
CRON_FILE="/etc/cron.d/unattended-upgrade-weekly"

echo "$CRON_JOB" | sudo tee "$CRON_FILE" > /dev/null
sudo chmod 644 "$CRON_FILE"

echo "✅ Unattended upgrades are scheduled and enabled!"
