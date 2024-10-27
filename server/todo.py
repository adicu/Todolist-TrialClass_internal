from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")

db = client['tasks']

Personal = db["Personal"]

db.Personal.insert_one({
    "taskID": 1, 
    "taskName": "testName", 
    "taskDescription": "testDesc", 
    "taskPriority": 0, 
    "taskStatus": False,
    "completionDate": "2024-10-31",
    "creationDate": "2024-10-27",
    "parentID": 2,})

collection_list = db.list_collections()
for c in collection_list:
    print(c)

