from telethon import TelegramClient, events
from datetime import datetime
import json
from telethon.tl.types import User, Channel
import os

colors = {
    "red": '\033[00;31m',
    "green": '\033[00;32m',
    "light_green": '\033[01;32m',
    "yellow": '\033[01;33m',
    "light_red": '\033[01;31m',
    "blue": '\033[94m',
    "purple": '\033[01;35m',
    "cyan": '\033[00;36m',
    "grey": '\033[90m',
}
messages = {
    "info1": f"{colors['red']}[{colors['light_green']}+{colors['red']}] {colors['light_green']}",
    "info2": f"{colors['red']}[{colors['yellow']}+{colors['red']}] {colors['cyan']}",
    "error": f"{colors['red']}[{colors['light_red']}-{colors['red']}] {colors['light_red']}",
}
SESSION_NAME = input(f"{messages['info1']}Enter the file name 'session' without any format: ")  
LOG_FILE = 'logs.json'

def save_message(message_dict):
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []

    data.append(message_dict)

    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

client = TelegramClient(SESSION_NAME, 726764276, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaa')

@client.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()

    msg_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    full_name = "Unknown"
    username = "N/A"

    if isinstance(sender, User):
        name = sender.first_name or ""
        last = sender.last_name or ""
        full_name = (name + " " + last).strip()
        username = sender.username or "N/A"
    elif isinstance(sender, Channel):
        full_name = sender.title or "Channel"
        username = "N/A"

    message_data = {
        "time": msg_time,
        "sender_name": full_name,
        "username": username,
        "message": event.message.message
    }

    print(f"\n{colors['green']}🟢 New Message Received at {colors['cyan']}{msg_time}")
    print(f"{colors['green']}👤 From: {colors['yellow']}{full_name} (@{username})")
    print(f"{colors['green']}💬 Message: {colors['yellow']}{event.message.message}")

    save_message(message_data)


client.start()
os.system('cls || clear')

print(f"""{colors['green']}

 _  _                                    
| |(_)       _                           
| | _  ___ _| |_ _____ ____  _____  ____ 
| || |/___|_   _) ___ |  _ \| ___ |/ ___)
| || |___ | | |_| ____| | | | ____| |    
 \_)_(___/   \__)_____)_| |_|_____)_|    
                                         

{colors['yellow']}✅ Listening for messages... (Press Ctrl+C to stop)\n""")
client.run_until_disconnected()