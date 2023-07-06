
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://jjames71396:qUFaF5pYhmjxAxPD@cluster0.ldooqi5.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["db"]
collection = db["game"]

# Insert a document
#document = {"name": "Player1", "stones": 3, "turn": True}
#inserted_document = collection.insert_one(document)
#print("Inserted document ID:", inserted_document.inserted_id)

# Query the document
query = {"name": "Player1"}
result = collection.find_one(query)
print("Queried document:", result)

query = {"name": "Player1"}
new_values = {"$set": {"turn": False}}
result = collection.update_one(query, new_values)
print("Matched documents:", result.matched_count)
print("Modified documents:", result.modified_count)

# Query the updated document
updated_document = collection.find_one(query)
print("Updated document:", updated_document)


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)