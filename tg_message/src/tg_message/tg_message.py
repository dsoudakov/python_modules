"""Main module."""
import requests
import os

def send_message(text):
    if not text:
        raise ValueError("Message is empty. No action taken.")

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        raise EnvironmentError("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variables not set.")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()  # Return response data as JSON
    except requests.exceptions.RequestException as e:
        # Log error with traceback
        print(f"Failed to send message: {e}")
        return None
