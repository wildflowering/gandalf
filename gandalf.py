import os
import csv
import requests
from datetime import datetime, timedelta
import pytz

# Load Discord Webhook URL from environment variable
webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

# Function to determine if the given date is in Week A or Week B
def get_week_type(start_date, target_date):
    # Calculate number of weeks since start_date
    weeks_elapsed = (target_date - start_date).days // 7
    return 'B' if weeks_elapsed % 2 == 0 else 'A'

# Function to load roster and filter based on the next day's schedule
def load_roster():
    schedule = []
    with open('roster.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if any(row.values()):  # Skip empty rows
                schedule.append(row)
    return schedule

# Function to send a message to Discord
def send_discord_message(content):
    data = {"content": content}
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Message sent successfully.")
    else:
        print("Failed to send message:", response.status_code, response.text)

# Main function to check roster and send notifications for the next day's duties
def notify_next_day_duties():
    # Set Sydney timezone
    sydney_tz = pytz.timezone("Australia/Sydney")
    
    # Get current time in Sydney
    now_sydney = datetime.now(sydney_tz)
    next_day = now_sydney + timedelta(days=1)  # Get the next day
    weekday = next_day.strftime("%A")
    date_str = next_day.strftime("%d/%m/%Y")
    
    # Define the starting date as Tuesday of Week B (05/11/24)
    start_date = datetime(2024, 11, 6).date()
    week_type = get_week_type(start_date, next_day.date())
    
    # Load the schedule
    schedule = load_roster()
    
    # Collect users for morning and afternoon duties
    duties = {
        'morning': [],
        'afternoon': []
    }
    
    # Filter based on the next day's weekday, week type, and time of day
    for entry in schedule:
        if entry['day'] == weekday and entry['week_type'] == week_type:
            duty_time = entry['time_of_day']
            duties[duty_time].append(f"<@{entry['user_id']}>")
    
    # Construct the message
    message_parts = []
    message_parts.append("**Morning:**")
    message_parts.append(", ".join(duties['morning']) if duties['morning'] else "None")
    message_parts.append("\n**Afternoon:**")
    message_parts.append(", ".join(duties['afternoon']) if duties['afternoon'] else "None")
    message_parts.append(f"\n- Duties for {date_str}")
    
    # Send message if there are duties for the next day
    if any(duties[time_of_day] for time_of_day in duties):
        message_content = "\n".join(message_parts)
        send_discord_message(message_content)
    else:
        print("No duties scheduled for the next day.")

# Run the notification function at 9 PM Sydney time daily
if __name__ == "__main__":
    notify_next_day_duties()
