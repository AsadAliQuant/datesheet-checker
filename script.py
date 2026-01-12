import requests
import urllib3
from bs4 import BeautifulSoup

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


if __name__ == "__main__":
    main()