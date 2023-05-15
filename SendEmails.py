import os
import json
import main

from email.message import EmailMessage
from config import *
import ssl
import smtplib
from email.message import EmailMessage
context = ssl.create_default_context()

email_sender = emailUser
email_password = emailPW
email_reciever = 'austintdriver@gmail.com'

#get documents from mongo
quotes = main.returnRandomQuote()

print (quotes)

subject = 'Hello from python'
body = quotes



msg = EmailMessage()
msg['From'] = email_sender
msg['To'] = email_reciever
msg['Subject'] = subject
msg.set_content(body, charset='utf-8')



with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_reciever, msg.as_string())


smtp.send_message(msg)

