import mongoOps
import SendEmails 

emailNames = ['']


email_recipients = emailNames
contentOfQuote = "this is a test. Delete mex2"
folder_path = 'comics/1995/12'  # Replace with the actual folder path containing the images

SendEmails.sendEmail(email_recipients)
# mongoOps.findAllQuotes()

#mongoOps.insertImage('comics/1995/01/19950101.gif')

#mongoOps.retrieveImage

    # --- insert images into mongo ---
#mongoOps.insertImagesFromFolderToMongo(folder_path)