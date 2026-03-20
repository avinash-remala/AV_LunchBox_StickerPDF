#!/usr/bin/env python3
"""
Send today's lunch summary and PDF via Zoho Mail.

Required environment variables:
    EMAIL_USERNAME      - Zoho Mail address to send from
    EMAIL_PASSWORD  - Zoho Mail password (or app-specific password)
    EMAIL_TO        - Recipient email addresses, comma-separated
"""

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

CST = ZoneInfo("America/Chicago")


def send_email(email_user: str, email_password: str, recipients: list, subject: str, body: str, pdf_path: str = None):
    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    if pdf_path:
        with open(pdf_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={Path(pdf_path).name}",
        )
        msg.attach(part)

    with smtplib.SMTP_SSL("smtp.zoho.com", 465) as server:
        server.login(email_user, email_password)
        server.sendmail(email_user, recipients, msg.as_string())


def main():
    email_user = os.environ.get("EMAIL_USERNAME")
    email_password = os.environ.get("EMAIL_PASSWORD")
    email_to = os.environ.get("EMAIL_TO")

    if not all([email_user, email_password, email_to]):
        print("✗ Missing required environment variables: EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_TO")
        sys.exit(1)

    now = datetime.now(CST)
    today = now.strftime("%Y-%m-%d")
    send_time = now.strftime("%m/%d %I:%M %p CST")
    export_dir = Path("exports") / today

    pdf_files = sorted(export_dir.glob("*.pdf"))
    txt_files = sorted(export_dir.glob("*.txt"))

    if not pdf_files or not txt_files:
        print(f"✗ No export files found in {export_dir}")
        sys.exit(1)

    pdf_path = str(pdf_files[-1])
    summary_text = txt_files[-1].read_text()

    send_pdf = os.environ.get("SEND_PDF", "false").lower() == "true"

    recipients = [e.strip() for e in email_to.split(",") if e.strip()]
    subject = f"Lunch Orders — {send_time}"

    print(f"Sending email to {len(recipients)} recipient(s)...")
    send_email(
        email_user,
        email_password,
        recipients,
        subject,
        summary_text,
        pdf_path=pdf_path if send_pdf else None,
    )
    print(f"✓ Done {'(with PDF attachment)' if send_pdf else '(summary only)'}")


if __name__ == "__main__":
    main()
