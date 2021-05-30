from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from sys import argv
from Agile.settings import EMAIL_HOST_USER
def send_mail():
    try:
        send_mail('Jenkins Build Failed', 'The last build failed, check it!', EMAIL_HOST_USER, ['yarinaf1@gmail.com','gaico070@gmail.com'], fail_silently=True)
