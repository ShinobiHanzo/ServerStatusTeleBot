import requests, time, datetime, subprocess
from data import TOKEN, CHAT_ID


import subprocess
import requests

# Telegram bot token
#TOKEN = BotToken

# Chat ID where notifications will be sent
#CHAT_ID = cID

# Function to send message to Telegram
def send_message(message):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    params = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, params=params)

# Function to notify about SSH login
def notify_ssh_login(username, ip_address):
    message = f'New SSH login:\nUsername: {username}\nIP Address: {ip_address}'
    send_message(message)

# Function to continuously monitor SSH login events
def monitor_ssh_logins():
    # Command to monitor SSH login events in real-time
    ssh_process = subprocess.Popen(['journalctl', '-f', '-n', '0', '_SYSTEMD_UNIT=sshd.service'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Continuously monitor SSH login events
    while True:
        line = ssh_process.stdout.readline().strip()
        if line:
            # Parse the line to extract SSH login details
            if 'Accepted password' in line:
                parts = line.split()
                username = parts[10]
                ip_address = parts[12]
                # Notify about SSH login
                notify_ssh_login(username, ip_address)


def notify_boot():
    send_message(message = "Server has completed boot.")

# Main function to start monitoring SSH login events
if __name__ == '__main__':
    # Notify when server completes boot
    notify_boot()
    monitor_ssh_logins()
