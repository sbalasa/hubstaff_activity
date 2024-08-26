import configparser

from constants import CONFIG_PATH
from datetime import datetime, timedelta

config = configparser.ConfigParser()
config.read(CONFIG_PATH)
app_token = config["hubstaff"]["app_token"]
auth_token = config["hubstaff"]["auth_token"]


def get_headers():
    return {"AppToken": app_token, "AuthToken": auth_token}


def get_yesterday():
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def format_time_spent(total_seconds):
    time_delta = timedelta(seconds=total_seconds)
    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
