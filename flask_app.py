from flask import Flask, render_template_string
from pymongo import MongoClient
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path='.env')

app = Flask(__name__)

# Get the MongoDB connection string from environment variables
mongo_connection_string = os.getenv('MONGODB_CONNECTION_STRING')

# Replace the connection string with your MongoDB connection string
client = MongoClient(mongo_connection_string)
db = client['test']
collection = db['datas']

def flatten_document(doc, parent_key='', sep='_'):
    flat_doc = {}
    for key, value in doc.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            flat_doc.update(flatten_document(value, new_key, sep=sep))
        elif isinstance(value, list):
            flat_doc[new_key] = ', '.join(map(str, value))
        else:
            flat_doc[new_key] = value
    return flat_doc

GITHUB_PAGE_URL = "https://rahuddev.github.io/x-data/"

@app.route('/')
def index():
    # Fetch all documents from the collection
    documents = collection.find()
    # Convert documents to a list of dictionaries and flatten them
    data = [flatten_document(doc) for doc in documents]
    response = requests.get(GITHUB_PAGE_URL)
    return render_template_string(response.text, data=data)

if __name__ == '__main__':
    app.run(debug=True)
