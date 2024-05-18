import asyncio
import os
import re
from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot
load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
allowed_user_ids = list(map(int, os.getenv("USERS").split('|')))
attacks = os.getenv("ATTACKS", "").split('|')
priorities = os.getenv("PRIORITY", "").split('|')

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
            if event_timestamp and event_timestamp > start_time:
                if priorities and priorities != ['']:
                    priority_value = get_log_priority(line)
                    if priority_value and str(priority_value) in priorities:
                        for user_id in allowed_user_ids:
                            message = (
                                            f"*HIGH PRIORITY EVENT (Priority {priority_value}) DETECTED:*\n"
                                            f"```\n{line.strip()}\n```"
                                        )
                            await send_telegram_message(user_id,message)
                elif attacks and attacks != ['']:
                    attack_id_match = re.search(r'\[1:(\d+):[0-9]+\]', line)
                    if attack_id_match:
                        attack_id = attack_id_match.group(1)
                        if attack_id in attacks:
                            for user_id in allowed_user_ids:
                                message = (
                                    f"*NEW ATTACK DETECTED:*\n"
                                    f"*Attack ID:* `{attack_id}`\n"
                                    f"```\n{line.strip()}\n```"
                                )
                                await send_telegram_message(user_id,message)
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
