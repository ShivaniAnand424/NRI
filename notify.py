"""Email alerts to the NRIPMC team, sent through Resend's HTTPS API.

Render's free plan blocks SMTP ports, so Gmail/Outlook SMTP cannot be used there.
Needs these environment variables:
    RESEND_API_KEY    API key from resend.com (starts with re_)
    ALERT_EMAIL_TO    where alerts go (comma-separate several addresses)
    ALERT_EMAIL_FROM  optional; default is Resend's test sender
"""
import json
import logging
import os
import threading
import urllib.error
import urllib.request

log = logging.getLogger(__name__)
API_URL = "https://api.resend.com/emails"


def _send(subject, body):
    api_key = os.environ.get("RESEND_API_KEY")
    recipients = [a.strip() for a in os.environ.get("ALERT_EMAIL_TO", "").split(",") if a.strip()]
    if not api_key or not recipients:
        log.warning("Email alert skipped: RESEND_API_KEY or ALERT_EMAIL_TO is not set")
        return

    payload = {
        "from": os.environ.get("ALERT_EMAIL_FROM", "NRIPMC Website <onboarding@resend.dev>"),
        "to": recipients,
        "subject": subject,
        "text": body,
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "nripmc-website/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            log.warning("Email alert sent (HTTP %s)", response.status)
    except urllib.error.HTTPError as error:
        log.error("Email alert rejected: HTTP %s %s", error.code, error.read().decode("utf-8", "ignore"))
    except Exception:
        log.exception("Could not send email alert")


def send_alert(subject, body):
    """Sends in the background so the customer's page is never delayed or broken."""
    threading.Thread(target=_send, args=(subject, body), daemon=True).start()