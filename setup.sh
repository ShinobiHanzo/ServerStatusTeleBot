#!/bin/bash

# Replace with the path to your Python script
PYTHON_SCRIPT="./notify.py"

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