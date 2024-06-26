import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(subject, body):
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = 587
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL')
    to_email = os.getenv('TO_EMAIL')
   
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    to_emails = to_email.split(',')
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        print("body: ", body)
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(from_email, to_emails, text)
        server.quit()
        print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')
        raise e