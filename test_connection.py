
from pymongo import MongoClient

# 1. Connect to the local MongoDB server on the specific port
client = MongoClient("mongodb://localhost:27012/")

# 2. Select your database and collection
db = client["csdb"]
collection = db["students"]

# 3. Run a query (Notice the syntax is very similar, but uses Python dictionaries)
student = collection.find_one({"name": "Liza"})

# 4. Print the result
print("Connection Successful! Found student:")
print(student)

# 5. Close the connection
client.close()
