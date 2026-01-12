import os

import requests
import urllib3
from bs4 import BeautifulSoup
from twilio.rest import Client

URL = "https://datesheet.vu.edu.pk"
TARGET_TEXT = "Date Sheet is not yet Launched"

# Set to False only if you hit local cert issues. True is default and safer.
VERIFY_CERT = False


def main():
    try:
        if not VERIFY_CERT:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        resp = requests.get(URL, timeout=10, verify=VERIFY_CERT)

        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"Error fetching page: {exc}")
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    msg = soup.find(id="lblDisplayMsg")
    text = msg.get_text(strip=True) if msg else ""

    if text == TARGET_TEXT:
        print("Date sheet not launched yet.")
    else:
        print("Please create your datesheet now as it's launched now.")
        trigger_call()


def trigger_call():
    sid = os.environ.get("TWILIO_ACCOUNT_SID")
    token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_number = os.environ.get("TWILIO_FROM_NUMBER")
    to_number = os.environ.get("TWILIO_TO_NUMBER")

    if not all([sid, token, from_number, to_number]):
        print("Twilio env vars missing; skipping call.")
        return

    client = Client(sid, token)
    try:
        call = client.calls.create(
            to=to_number,
            from_=from_number,
            twiml="<Response><Say>Date sheet is now launched. Please create your date sheet.</Say></Response>",
        )
        print(f"Triggered call: {call.sid}")
    except Exception as exc:  # Twilio may raise generic TwilioRestException
        print(f"Failed to place call: {exc}")


if __name__ == "__main__":
    main()