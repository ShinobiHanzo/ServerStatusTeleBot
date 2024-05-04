setup the server's settings before continuing the service:

start by preparing the required libraries:

// in linux terminal
sudo apt-get install python3-pip
sudo pip3 install -r requirements.txt



make sure you update the information within the data.py to confirm the setting for your bot:

// data.py
TOKEN = '<YOUR_API_TOKEN_HERE>'
CHAT_ID = '<YOUR_PERSONAL_CHAT_ID_HERE>'
BOT_USERNAME = '<BOT_USERNAME_HERE>'


After updating the settings in "data.py", add the files to system's control:

// in linux terminal
sudo systemctl enable notify
sudo systemctl start notify


Make sure you're in the local directory before starting any of the process