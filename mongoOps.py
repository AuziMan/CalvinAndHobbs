import config
import random

from pymongo import MongoClient

connection_string = config.db_connection_string
client = MongoClient(connection_string)
db = client.list_database_names()
print(db)
quotes_db = client.Quotes
collections = quotes_db.list_collection_names()
print(collections)


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
    foundQuotes = collection.find()
    for docs in foundQuotes:
        print(docs)


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


