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
email_reciever = 'austintdriver@gmail.com', 'tom.driver@gmail.com'

#get documents from mongo
quotes = main.returnRandomQuote()

print (quotes)

subject = 'Daily Calvin and Hobbs Quote and comic!'
body = 'Quote of the day:    ' + quotes



msg = EmailMessage()
msg['From'] = email_sender
msg['To'] = email_reciever
msg['Subject'] = subject
msg.set_content(body, charset='utf-8')

image_path = 'media/19950102.jpg'
with open(image_path, 'rb') as file:
    image_data = file.read()

image_filename = os.path.basename(image_path)


msg.add_attachment(image_data, maintype='image', subtype='jpg', filename = image_filename )


with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_reciever, msg.as_string())


smtp.send_message(msg)

