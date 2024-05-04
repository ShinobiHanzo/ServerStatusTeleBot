from typing import Final
import requests, time, datetime, subprocess
from data import TOKEN, CHAT_ID, BOT_USERNAME
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN: Final = 'TOKEN'
BOT_USERNAME = ''


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I will be your personal assistant bot managing the server you installed me in.\nA pleasure to work with you!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Your server is currently running! what would you like me to do?")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("this is a custom command")

async def reboot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Rebooting...")
    try:
        subprocess.run(["sudo", "reboot"])
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


# Automatic Nofications

def send_notification(message):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)

def notify_boot():
    send_notification(message = "Server has completed boot.")

def notify_ssh_login(username, ip_address):
    message = f'New SSH login:\nUsername: {username}\nIP Address: {ip_address}'
    send_notification(message)



# Responses

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hello there!'
    if 'time' in processed:
        return 'Time is ' + str(datetime.now())
    if 'how are you' in processed:
        return f'your server is running fine'
    return 'I do not understand.'



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replave(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {update} caused arror {context.error}')

if __name__ =='__main__':

    # Notify when server completes boot
    notify_boot()

    # Get SSH login details
    ssh_details = subprocess.run(['last', '-i', '-F'], capture_output=True, text=True).stdout
    # Parse the output to get the last SSH login
    last_ssh_login = ssh_details.splitlines()[1].split()
    username, ip_address = last_ssh_login[0], last_ssh_login[2]
    # Notify about SSH login
    notify_ssh_login(username, ip_address)





    app = Application.builder().token(TOKEN).build()


    # Commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('custom',custom_command))
    app.add_handler(CommandHandler('reboot',reboot_command))


    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval = 3)