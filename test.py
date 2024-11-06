
import requests
import json

# Replace 'YOUR_WEBHOOK_URL' with your actual webhook URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/1303302088905850960/BksSWu0n6HM1TL1AhMKR7j9QpyIjldlmFokmi1ZonCYPF_4s4BO-RVbs5HQ9OUCwgNEC'

# The message you want to send
data = {
    "content": "you're welcome"
}

# Send the message to the webhook
response = requests.post(WEBHOOK_URL, json=data)

# Check for successful response
if response.status_code == 204:
    print("Message sent successfully!")
else:
    print(f"Failed to send message: {response.status_code}, {response.text}")
