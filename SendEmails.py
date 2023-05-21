import os
import ssl
import smtplib
from email.message import EmailMessage
from config import *
import mongoOps

def sendEmail(recipients):
    # Retrieve a random quote from mongoOps
    quote = mongoOps.returnRandomQuote()

    # Email configuration
    email_sender = emailUser
    email_password = emailPW
    subject = 'Daily Calvin and Hobbs Quote and Comic!'
    body = 'Quote of the day: ' + quote

    # Create the email message
    msg = EmailMessage()
    msg['From'] = email_sender
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    msg.set_content(body, charset='utf-8')

    # Retrieve the comic image from MongoDB
    image_file_id = mongoOps.retrieveImage()

    # Add the comic image as an attachment
    image_path = 'media/tempImages/' + image_file_id  # Adjust the image path as needed
    with open(image_path, 'rb') as file:
        image_data = file.read()
    image_filename = os.path.basename(image_path)
    msg.add_attachment(image_data, maintype='image', subtype='jpg', filename=image_filename)

    # SMTP server connection and email sending
    context = ssl.create_default_context()
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.login(email_sender, email_password)
        smtp.send_message(msg)
