import requests
from bs4 import BeautifulSoup
from colorama import init
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from time import sleep
import os

init(autoreset=True)
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
print (f"""{colors['yellow']}

  ________  _______   ________  ________  __      ______    _____  ___   
 /"       )/"     "| /"       )/"       )|" \    /    " \  (\"   \|"  \  
(:   \___/(: ______)(:   \___/(:   \___/ ||  |  // ____  \ |.\\   \    | 
 \___  \   \/    |   \___  \   \___  \   |:  | /  /    ) :)|: \.   \\  | 
  __/  \\  // ___)_   __/  \\   __/  \\  |.  |(: (____/ // |.  \    \. | 
 /" \   :)(:      "| /" \   :) /" \   :) /\  |\\        /  |    \    \ | 
(_______/  \_______)(_______/ (_______/ (__\_|_)\"_____/    \___|\____\) 
                                                                         
    {colors['red']}Tg: @Mresfelurm\n\n
""")
phone_number = input(f"{messages['info1']}Enter your phone number (e.g. +1XXXXXXXX): {colors['red']}").strip()

with requests.Session() as req:
    login0 = req.post('https://my.telegram.org/auth/send_password', data={'phone': phone_number})

    if 'Sorry, too many tries' in login0.text:
        print(f'{colors["red"]}Too many tries. Try again later.')
        exit()

    login_data = login0.json()
    random_hash = login_data['random_hash']

    code = input(f"{messages['info1']}Enter the code sent via Telegram: {colors['red']}").strip()

    login_data = {
        'phone': phone_number,
        'random_hash': random_hash,
        'password': code
    }

    login = req.post('https://my.telegram.org/auth/login', data=login_data)
    apps_page = req.get('https://my.telegram.org/apps')
    soup = BeautifulSoup(apps_page.text, 'html.parser')

    api_id_tag = soup.find('label', string='App api_id:')
    if not api_id_tag:
        print(f"{colors['yellow']}[~] No app found. Creating a new one...")
        create_data = {
            'app_title': 'AutoApp',
            'app_shortname': 'autoapp' + phone_number[-4:],
            'app_url': 'https://example.com',
            'app_platform': 'android',
            'app_desc': 'Auto-generated Telegram app via Python script'
        }
        req.post('https://my.telegram.org/apps/create', data=create_data)
        apps_page = req.get('https://my.telegram.org/apps')
        soup = BeautifulSoup(apps_page.text, 'html.parser')

    try:
        api_id = soup.find('label', string='App api_id:').find_next_sibling('div').select_one('span').get_text(strip=True)
        api_hash = soup.find('label', string='App api_hash:').find_next_sibling('div').select_one('span').get_text(strip=True)
        print(f"""{colors['green']}
✅ API Credentials:
{colors['green']}  [✓] API ID: {colors['yellow']}{api_id}
{colors['green']}  [✓] API HASH: {colors['yellow']}{api_hash}
""")
    except Exception as e:
        print(f'{colors["red"]}⚠️ Could not extract API info. Error: {e}')
        exit()
print (f"{colors['green']} Enter the code sent to your account")
session_name = phone_number.replace("+", "") 
client = TelegramClient(session_name, int(api_id), api_hash)

try:
    client.start(phone=phone_number)
    me = client.get_me()
    print(f"""{colors['green']}
🟢 Logged in successfully as:
  👤 Name: {me.first_name} {me.last_name or ""}
  🆔 ID: {me.id}
  🔗 Username: @{me.username or "N/A"}
  💾 Session saved as: {session_name}.session
""")
except SessionPasswordNeededError:
    password = input(f"{colors['yellow']}[!] 2FA Password Required: ")
    client.sign_in(password=password)
    print(f"{colors['green']}✔ Logged in with 2FA successfully.")

client.disconnect()
