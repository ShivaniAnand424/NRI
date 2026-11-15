"""Email alerts to the NRIPMC team, sent through Resend's HTTPS API.

Render's free plan blocks SMTP ports, so Gmail/Outlook SMTP cannot be used there.
Needs these environment variables:
    RESEND_API_KEY    API key from resend.com (starts with re_)
    ALERT_EMAIL_TO    where alerts go (comma-separate several addresses)
    ALERT_EMAIL_FROM  optional; default is Resend's test sender
"""
import logging
import os
import smtplib
import ssl
import threading
from email.message import EmailMessage

log = logging.getLogger(__name__)


def _send(subject, body):
    host = os.environ.get("SMTP_HOST", "smtp.hostinger.com")
    port = int(os.environ.get("SMTP_PORT", "465"))
    user = os.environ.get("SMTP_USER", "")
    password = os.environ.get("SMTP_PASSWORD", "")
    sender = os.environ.get("SMTP_FROM") or user
    recipient = os.environ.get("ALERT_TO") or user

    if not (user and password and recipient):
        log.warning("Alert email skipped: SMTP_USER / SMTP_PASSWORD / ALERT_TO not set in .env")
        return False

    message = EmailMessage()
    message["Subject"] = " ".join(subject.split())
    message["From"] = sender
    message["To"] = recipient
    message.set_content(body)

    try:
        context = ssl.create_default_context()
        if port == 465:
            with smtplib.SMTP_SSL(host, port, context=context, timeout=15) as server:
                server.login(user, password)
                server.send_message(message)
        else:
            with smtplib.SMTP(host, port, timeout=15) as server:
                server.starttls(context=context)
                server.login(user, password)
                server.send_message(message)
        return True
    except Exception:
        log.exception("Could not send alert email")
        return False


def send_alert(subject, body):
    threading.Thread(target=_send, args=(subject, body), daemon=True).start()


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    ok = _send("NRIPMC test email", "If you can read this, your website email alerts work.")
    print("SENT OK - check your inbox" if ok else "FAILED - see the error above")