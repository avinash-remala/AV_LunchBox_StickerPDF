#!/usr/bin/env python3
"""
Send today's lunch PDF and summary via WhatsApp using Twilio.

Required environment variables:
    TWILIO_SID      - Twilio Account SID
    TWILIO_TOKEN    - Twilio Auth Token
    WHATSAPP_TO     - Recipient WhatsApp numbers, comma-separated (e.g. +12345678900,+19876543210)
"""

import os
import sys
import requests
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

CST = ZoneInfo("America/Chicago")


TWILIO_SANDBOX_NUMBER = "+14155238886"  # Twilio WhatsApp Sandbox number


def upload_pdf(pdf_path: str) -> str:
    """Upload PDF as a GitHub Release asset and return the public download URL."""
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")  # e.g. avinash-remala/AV_LunchBox_StickerPDF

    if not token or not repo:
        raise RuntimeError("GITHUB_TOKEN and GITHUB_REPOSITORY must be set")

    today = datetime.now(CST).strftime("%Y-%m-%d")
    tag = f"lunch-{today}"
    filename = Path(pdf_path).name
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Get or create a release for today
    release_resp = requests.get(
        f"https://api.github.com/repos/{repo}/releases/tags/{tag}", headers=headers
    )
    if release_resp.status_code == 404:
        release_resp = requests.post(
            f"https://api.github.com/repos/{repo}/releases",
            headers=headers,
            json={"tag_name": tag, "name": f"Lunch Orders {today}", "draft": False, "prerelease": False},
            timeout=30,
        )
    release = release_resp.json()
    if "upload_url" not in release:
        print(f"GitHub Release API error (status {release_resp.status_code}): {release}")
        raise RuntimeError(f"Failed to get/create GitHub Release: {release.get('message', 'unknown error')}")

    # Delete existing asset with same name if any (re-run case)
    for asset in release.get("assets", []):
        if asset["name"] == filename:
            requests.delete(
                f"https://api.github.com/repos/{repo}/releases/assets/{asset['id']}",
                headers=headers, timeout=30
            )

    # Upload PDF asset
    upload_url = release["upload_url"].replace("{?name,label}", f"?name={filename}")
    with open(pdf_path, "rb") as f:
        upload_resp = requests.post(
            upload_url,
            headers={**headers, "Content-Type": "application/pdf"},
            data=f,
            timeout=120,
        )
    upload_data = upload_resp.json()
    if upload_resp.status_code not in (200, 201) or "browser_download_url" not in upload_data:
        print(f"PDF upload failed (status {upload_resp.status_code}): {upload_data}")
        raise RuntimeError(f"Failed to upload PDF asset: {upload_data.get('message', 'unknown error')}")
    return upload_data["browser_download_url"]


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
    today = datetime.now(CST).strftime("%Y-%m-%d")
    export_dir = Path("exports") / today

    pdf_files = sorted(export_dir.glob("*.pdf"))
    txt_files = sorted(export_dir.glob("*.txt"))

    if not pdf_files or not txt_files:
        print(f"✗ No export files found in {export_dir}")
        sys.exit(1)

    pdf_path = str(pdf_files[-1])   # Most recent
    summary_text = txt_files[-1].read_text()

    send_pdf = os.environ.get("SEND_PDF", "false").lower() == "true"

    # Import Twilio (installed in workflow)
    from twilio.rest import Client
    client = Client(account_sid, auth_token)

    if send_pdf:
        # Upload PDF and get public URL
        print(f"Uploading PDF: {pdf_path}")
        pdf_url = upload_pdf(pdf_path)
        print(f"PDF URL: {pdf_url}")
        message = f"{summary_text}\n\n📄 PDF: {pdf_url}"
    else:
        message = summary_text

    # Send to all recipients (comma-separated numbers)
    recipients = [n.strip() for n in to_number.split(",") if n.strip()]
    print(f"Sending to {len(recipients)} recipient(s)...")

    for number in recipients:
        print(f"  → {number}")
        send_message(client, number, body=message)
        if send_pdf:
            send_message(client, number, body="📎 Lunch PDF attached:", media_url=pdf_url)

    print("✓ Done")


if __name__ == "__main__":
    main()
