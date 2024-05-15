# Suricata Telegram Alerts 🚨📱

This Python script 🐍 monitors Suricata logs for specified attack IDs and sends alerts via Telegram when new attacks are detected.

## Requirements 📋

- Python 3.x 🐍
- `python-telegram-bot` library
- `python-dotenv` library

## Installation 💻

1. **Clone the repository:**

   ```bash
   git clone https://github.com/bugourmet/suricata-alerts
   ```

2. **Install the required python packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a .env file in the root directory of the project and add your bot token and user IDs in the format specified in the .env.sample file or Configuration section.**

4. **Run the script:**
   ```bash
   python3 monitor.py
   ```

## Configuration ⚙️

| Variable    | Description                                                     |
| ----------- | --------------------------------------------------------------- |
| `BOT_TOKEN` | Your Telegram bot token.                                        |
| `USERS`     | Pipe-separated list of user IDs for alerts.                     |
| `ATTACKS`   | Pipe-separated list of attack IDs to monitor.                   |
| `PRIORITY`  | Pipe-separated desired priority level to filter (e.g., `1,2,3`) |

Description of Parameters:

    PRIORITY: A pipe-separated string of desired priority levels to filter by (e.g., 1|2|3). This is optional. If provided, the program will check log entries for these priority levels and alert based on them. If not provided or left empty, the program will fall back to checking by attack IDs.
    ATTACKS: A list of attack IDs to filter by. This will be used if PRIORITY is not provided or is empty.
    ALLOWED_USER_IDS: A list of user IDs to send Telegram messages to. Ensure that these are valid Telegram user IDs.

## Contributing 🤝

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
