#!/usr/bin/env python3
"""
Send today's lunch PDF and summary via WhatsApp using Twilio.

Required environment variables:
    TWILIO_SID      - Twilio Account SID
    TWILIO_TOKEN    - Twilio Auth Token
    WHATSAPP_TO     - Recipient WhatsApp number (e.g. +12345678900)
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime


TWILIO_SANDBOX_NUMBER = "+14155238886"  # Twilio WhatsApp Sandbox number


def upload_pdf(pdf_path: str) -> str:
    """Upload PDF to transfer.sh and return the public URL."""
    filename = Path(pdf_path).name
    result = subprocess.run(
        ["curl", "-s", "--upload-file", pdf_path, f"https://transfer.sh/{filename}"],
        capture_output=True, text=True, timeout=60
    )
    url = result.stdout.strip()
    if not url.startswith("https://"):
        raise RuntimeError(f"Upload failed. Response: {url}")
    return url


def send_message(client, to_number: str, body: str = None, media_url: str = None):
    """Send a WhatsApp message via Twilio."""
    kwargs = {
        "from_": f"whatsapp:{TWILIO_SANDBOX_NUMBER}",
        "to": f"whatsapp:{to_number}",
    }
    if body:
        kwargs["body"] = body
    if media_url:
        kwargs["media_url"] = [media_url]
    return client.messages.create(**kwargs)


def main():
    # Load credentials from environment
    account_sid = os.environ.get("TWILIO_SID")
    auth_token = os.environ.get("TWILIO_TOKEN")
    to_number = os.environ.get("WHATSAPP_TO")

    if not all([account_sid, auth_token, to_number]):
        print("✗ Missing required environment variables: TWILIO_SID, TWILIO_TOKEN, WHATSAPP_TO")
        sys.exit(1)

    # Find today's export files
    today = datetime.now().strftime("%Y-%m-%d")
    export_dir = Path("exports") / today

    pdf_files = sorted(export_dir.glob("*.pdf"))
    txt_files = sorted(export_dir.glob("*.txt"))

    if not pdf_files or not txt_files:
        print(f"✗ No export files found in {export_dir}")
        sys.exit(1)

    pdf_path = str(pdf_files[-1])   # Most recent
    summary_text = txt_files[-1].read_text()

    # Import Twilio (installed in workflow)
    from twilio.rest import Client
    client = Client(account_sid, auth_token)

    # 1. Send summary as text message
    print("Sending summary via WhatsApp...")
    send_message(client, to_number, body=summary_text)
    print("✓ Summary sent")

    # 2. Upload PDF and send as media message
    print(f"Uploading PDF: {pdf_path}")
    pdf_url = upload_pdf(pdf_path)
    print(f"PDF URL: {pdf_url}")

    send_message(client, to_number, media_url=pdf_url)
    print("✓ PDF sent")


if __name__ == "__main__":
    main()
