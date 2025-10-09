import smtplib
import traceback
import os
import sys
import jinja2

sys.path.append(os.path.abspath("."))

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from typing import List, Dict

from app.src.adapters import (
    Email,
    Role,
    get_recipients,
    get_email_template,
    logger,
)

EMAIL_SUBJECT = "ETL-monitoring"


def make_email_message(
    message_from: str,
    message_to: List[str],
    message_param: Dict,
    message_template: jinja2.Template,
) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"] = message_from
    msg["To"] = ",".join(message_to)

    msg.attach(MIMEText(message_template.render(message_param), "html"))
    return msg


def send_email(message_param: Dict, message_template: str, role: Role) -> None:
    """Collect everything together.
    1. Message parameters
    2. SMTP server parameter
    3. Send message
    """
    email = Email()

    msg = make_email_message(
        message_from=email.sender,
        message_to=get_recipients(role),
        message_param=message_param,
        message_template=get_email_template(message_template),
    )
    with smtplib.SMTP(email.server, email.port) as server:
        server.starttls()
        server.login(email.username, email.password)
        server.send_message(msg)


def notify(message_param: Dict, message_template: str, role: Role = Role.ADMIN) -> None:
    """Entry point to notification."""
    try:
        logger.info(f"Role = {role.value}. Notification parameters {message_param}")
        send_email(message_param, message_template, role)
    except Exception as er:
        logger.info("got notification error")
        logger.info(f"notification error reason: {er}  {traceback.format_exc()}")
