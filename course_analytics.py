from pymongo import MongoClient

# 1. Connect and select the collection
client = MongoClient("mongodb://localhost:27012/")
db = client["csdb"]
collection = db["students"]

# 2. Define pipeline
pipeline = [
        { "$unwind": "$courses_taken" },
        { "$group": { "_id": "$courses_taken", "avg_GPA": { "$avg": "$gpa" } } },
        { "$sort": { "avg_GPA": -1} }
]

# 3. Execute the aggregation
print("--- Average GPA by Course ---")
results = collection.aggregate(pipeline)

# 4. Loop through the ccursor to print each document
for doc in results:
    print(f"Course: {doc['_id']} | Average GPA: {round(doc['avg_GPA'], 2)}")
client.close()    
