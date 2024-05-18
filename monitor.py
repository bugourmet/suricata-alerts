import asyncio
import os
import re
from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot
load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
allowed_user_ids = list(map(int, os.getenv("USERS").split(',')))
attacks = os.getenv("ATTACK_IDS", "").split(',')
ignore_list = os.getenv("IGNORED_ATTACK_IDS", "").split(',')
priorities = os.getenv("PRIORITY", "").split(',')

async def send_telegram_message(user_id, message):
    """Sends a Telegram message."""
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=user_id, text=message,parse_mode='Markdown')

def parse_log_timestamp(log_line):
    timestamp_match = re.search(r'\d{2}/\d{2}/\d{4}-\d{2}:\d{2}:\d{2}\.\d{6}', log_line)
    if timestamp_match:
        timestamp_str = timestamp_match.group()
        timestamp = datetime.strptime(timestamp_str, '%m/%d/%Y-%H:%M:%S.%f')
        return timestamp
    else:
        return None

def get_log_priority(log_line):
    priority_match = re.search(r'\[Priority: (\d+)\]', log_line)
    if priority_match:
        return int(priority_match.group(1))
    return None

async def check_log_file(filename, start_time):
    with open(filename, "r") as f:
        for line in f:
            event_timestamp = parse_log_timestamp(line)
            if not event_timestamp or event_timestamp <= start_time:
                continue

            priority_value = get_log_priority(line)
            attack_id_match = re.search(r'\[1:(\d+):[0-9]+\]', line)
            attack_id = attack_id_match.group(1)
            if priorities and priorities != [''] and priority_value and str(priority_value) in priorities and attack_id not in ignore_list:
                for user_id in allowed_user_ids:
                    message = (
                        f"*HIGH PRIORITY EVENT (Priority {priority_value}) DETECTED:*\n"
                        f"```perl\n{line.strip()}\n```"
                    )
                    await send_telegram_message(user_id, message)
            elif attacks and attacks != [''] and attack_id_match:
                attack_id = attack_id_match.group(1)
                if attack_id in attacks and attack_id not in ignore_list:
                    for user_id in allowed_user_ids:
                        message = (
                            f"*NEW ATTACK DETECTED:*\n"
                            f"*Attack ID:* `{attack_id}`\n"
                            f"```perl\n{line.strip()}\n```"
                        )
                        await send_telegram_message(user_id, message)
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
