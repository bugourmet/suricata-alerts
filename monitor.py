import os
import re
import asyncio
from telegram import Bot
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
allowed_user_ids = list(map(int, os.getenv("USERS").split('|')))
attacks = os.getenv("ATTACKS").split('|')

async def send_telegram_message(user_id, message):
    """Sends a Telegram message."""
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=user_id, text=message)

def parse_log_timestamp(log_line):
    timestamp_match = re.search(r'\d{2}/\d{2}/\d{4}-\d{2}:\d{2}:\d{2}\.\d{6}', log_line)
    if timestamp_match:
        timestamp_str = timestamp_match.group()
        timestamp = datetime.strptime(timestamp_str, '%m/%d/%Y-%H:%M:%S.%f')
        return timestamp
    else:
        return None

async def check_log_file(filename, start_time):
    with open(filename, "r") as f:
        for line in f:
            event_timestamp = parse_log_timestamp(line)
            if event_timestamp and event_timestamp > start_time:
                attack_id_match = re.search(r'\[1:(\d+):[0-9]+\]', line)
                if attack_id_match:
                    attack_id = attack_id_match.group(1)
                    if attack_id in attacks:
                        for user_id in allowed_user_ids:
                            await send_telegram_message(user_id, f"NEW ATTACK DETECTED: {line}")
                else:
                    pass
        start_time = datetime.now()
    return start_time

async def main() -> None:
    """Main function to monitor logs and send alerts."""
    start_time = datetime.now() 
    print("Alerting is enabled. Monitoring for attacks...")
    for user_id in allowed_user_ids:
        await send_telegram_message(user_id, "Alerting enabled. Monitoring for attacks...")
    while True:
        start_time = await check_log_file("/var/log/suricata/fast.log", start_time)

if __name__ == "__main__":
    asyncio.run(main())
