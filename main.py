import mongoOps
import SendEmails 

email_recipients = ['austintdriver@gmail.com']
contentOfQuote = "this is a test. Delete mex2"

SendEmails.sendEmail(email_recipients)
mongoOps.findAllQuotes()
