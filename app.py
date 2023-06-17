from flask import Flask
from flask.json import jsonify
from requests import request
import mongoOps
import json
import config
from pymongo import MongoClient
from gridfs import GridFS
import os
import random

app = Flask(__name__)

# MongoDB connection
connection_string = config.db_connection_string
client = MongoClient(connection_string)
quotes_db = client.Quotes

# Retrieve all quotes from MongoDB
@app.route('/quotes', methods=['GET'])
def get_quotes():

    quotes = mongoOps.findAllQuotes()
    quotes_body = []
    
    for i, quote in enumerate(quotes, start=1):
        quote_key = f"quote{i}"
        quotes_body.append({quote_key: quote})
        
    response =  {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "quotes": quotes_body
    }   

    return jsonify(response) 


# Insert image from folder to MongoDB
@app.route('/images/folder', methods=['POST'])
def insert_images_from_folder():
    folder_path = request.json['folder_path']
    fs = GridFS(quotes_db)
    comics_collection = quotes_db['comics']

    for filename in os.listdir(folder_path):
        if filename.endswith('.gif'):
            image_path = os.path.join(folder_path, filename)
            with open(image_path, 'rb') as file:
                data = file.read()
            file_id = fs.put(data, filename=filename)
            comics_collection.insert_one({"file_id": file_id, "filename": filename})

    return jsonify({"message": "Images added successfully"})

# Insert image into MongoDB
@app.route('/images', methods=['POST'])
def insert_image():
    image = request.json['image']
    fs = GridFS(quotes_db)

    with open(image, 'rb') as file:
        data = file.read()

    file_id = fs.put(data, filename=image)

    comics_collection = quotes_db['comics']
    comics_collection.insert_one({"file_id": file_id})

    return jsonify({"message": "Image added successfully"})

# Retrieve a random image from MongoDB
@app.route('/images/random', methods=['GET'])
def retrieve_random_image():
    fs = GridFS(quotes_db)
    comics_collection = quotes_db['comics']

    count = comics_collection.count_documents({})
    if count == 0:
        return jsonify({"message": "No images found"})

    random_index = random.randint(0, count - 1)
    random_doc = comics_collection.find().skip(random_index).limit(1)[0]
    file_id = random_doc.get("file_id", None)

    if file_id is None:
        return jsonify({"message": "No image found"})

    output_path = 'media/tempImages/' + str(file_id)  # Convert ObjectId to string

    grid_out = fs.get(file_id)

    with open(output_path, 'wb') as file_output:
        file_output.write(grid_out.read())

    return jsonify({"message": "Image retrieved successfully"})

# Insert quote into MongoDB
@app.route('/quotes', methods=['POST'])
def insert_quote():
    quote = request.json['quote']
    collection = quotes_db.listOfQuotes

    quotes = {
        "quoteTest": quote
    }

    inserted_id = collection.insert_one(quotes).inserted_id

    return jsonify({"message": "Quote added successfully"})


if __name__ == '__main__':
    app.run()