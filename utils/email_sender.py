import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "YOUR_EMAIL@gmail.com"
APP_PASSWORD = "YOUR_APP_PASSWORD"  # NOT normal password


def send_email(receiver_email, subject, body):

    if not receiver_email:
        return {"success": False, "message": "No recipient email provided"}

    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)

        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()

        return {"success": True, "email": receiver_email}

    except Exception as e:
        return {"success": False, "message": str(e)}