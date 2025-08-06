import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# You can keep these in a config file or environment variables for safety
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_ADDRESS = "hyadav7983@gmail.com"
EMAIL_PASSWORD = "Ganpati@112233"  # Use App Password if 2FA is enabled

def send_email(recipient_email, subject, message_body):
    try:
        # Create the email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = recipient_email
        msg["Subject"] = subject

        msg.attach(MIMEText(message_body, "plain"))

        # Send the email via SMTP
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {recipient_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
