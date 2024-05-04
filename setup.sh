#!/bin/bash

# Function to validate Telegram bot token
validate_token() {
    local token_length=${#1}
    local token_regex="^[0-9]{8}:[a-zA-Z0-9]{32}$"
    if [[ $1 =~ $token_regex ]]; then
        echo "Valid token."
        return 0
    else
        echo "Error: Token must be in the format ########:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        return 1
    fi
}

# Prompt user for Telegram bot token
read -p "Enter your Telegram bot token in the format ########:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx: " BOT_TOKEN

# Validate the token format
while ! validate_token "$BOT_TOKEN"; do
    read -p "Enter your Telegram bot token in the format ########:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx: " BOT_TOKEN
done

# Replace with the path to your Python script
PYTHON_SCRIPT="./notify.py"

# Replace with your Telegram chat ID
CHAT_ID="YOUR_CHAT_ID"

# Complete the service file template with the provided parameters
cat <<EOF > ssh_login_notifier.service
[Unit]
Description=SSH Login Notifier Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$(dirname "${PYTHON_SCRIPT}")
ExecStart=/usr/bin/python3 ${PYTHON_SCRIPT}
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Install pip requirements
pip3 install requests

echo "Service file created: ssh_login_notifier.service"
echo "Pip requirements installed"

sudo mv ssh_login_notifier.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ssh_login_notifier.service
sudo systemctl start ssh_login_notifier.service
cat ./README.me