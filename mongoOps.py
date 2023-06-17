import json
import config
from bson import json_util
import os

import random

from pymongo import MongoClient
from gridfs import GridFS

connection_string = config.db_connection_string
client = MongoClient(connection_string)
db = client.list_database_names()
print(db)
quotes_db = client.Quotes
collections = quotes_db.list_collection_names()
print(collections)

#insert image from folder
def insertImagesFromFolderToMongo(folder_path):
    connection_string = config.db_connection_string
    client = MongoClient(connection_string)
    db = client.Quotes  # Replace with the actual name of your database

    # Insert each image data into GridFS and save file ID in comics collection
    fs = GridFS(db)
    comics_collection = db['comics']  # Replace with the actual name of your collection

    for filename in os.listdir(folder_path):
        if filename.endswith('.gif'):
            image_path = os.path.join(folder_path, filename)
            with open(image_path, 'rb') as file:
                data = file.read()
            file_id = fs.put(data, filename=filename)
            comics_collection.insert_one({"file_id": file_id, "filename": filename})
            print("Image '{}' added!".format(filename))

    print("All images added!")

# insert comic
def insertImage(image):
    fs = GridFS(quotes_db)

    with open (image, 'rb') as file:
        data = file.read()
    
    file_id = fs.put(data, filename=image)

    comics_collection = quotes_db['comics']
    comics_collection.insert_one({"file_id": file_id})
    print("image added!")

# get all comics
def retrieveImage():
    connection_string = config.db_connection_string
    client = MongoClient(connection_string)
    db = client.Quotes
    collection = db.comics
    fs = GridFS(db)

    # Retrieve a random document from the collection
    random_doc = collection.aggregate([{ "$sample": { "size": 1 } }])
    doc = random_doc.next()
    file_id = doc.get("file_id", None)
    if file_id is None:
        raise ValueError("No random document found in the collection.")

    output_path = 'media/tempImages/' + str(file_id)  # Convert ObjectId to string

    grid_out = fs.get(file_id)

    with open(output_path, 'wb') as file_output:
        file_output.write(grid_out.read())

    return str(file_id)  # Convert ObjectId to string


# Insert quote function.
def insertQuotes(quote):
    collection = quotes_db.listOfQuotes
    #insert quote below with similar format
    quotes = {
        "quoteTest": quote
    }
    inserted_id = collection.insert_one(quotes).inserted_id
    print(inserted_id)


# Print all quotes from the database
def findAllQuotes():
    collection = quotes_db.listOfQuotes
    foundQuotes = collection.find({}, {"_id": 0})
    quotes_list = []

    for docs in foundQuotes:
        quote = next(iter(docs.values()))

        quotes_list.append(quote)

    return quotes_list   


# returns the quote based on the ID of the quote. 
def returnOneQuote():
    collection = quotes_db.listOfQuotes
    foundQuote = collection.find_one()
    print(foundQuote['quote1'])
    return foundQuote['quote1']  


# Returns a random Quote
def returnRandomQuote():
    collection = quotes_db.listOfQuotes
    count = collection.count_documents({})
    if count == 0:
        return None
    random_index = random.randint(0, count - 1)
    found_quote = collection.find().skip(random_index).limit(1)[0]
    quote_keys = [key for key in found_quote.keys() if key.startswith('quote')]
    if len(quote_keys) == 0:
        return None
    random_quote_key = random.choice(quote_keys)
    random_quote = found_quote[random_quote_key]
    print(random_quote)
    return random_quote


