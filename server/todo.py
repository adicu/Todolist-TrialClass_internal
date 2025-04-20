from pymongo import MongoClient

connection_string = "mongodb+srv://user:qwertyuiop@cluster0.ypdasjk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_string, tlsAllowInvalidCertificates=True)

db = client['To-do']

tasks = db["Tasks"]
lists = db["Lists"]

db.Tasks.insert_one({
    "taskID": 1, 
    "taskName": "testName", 
    "taskDescription": "testDesc", 
    "taskPriority": 0, 
    "taskStatus": False,
    "completionDate": "2024-10-31",
    "creationDate": "2024-10-27",
    "parentID": 1})

db.Lists.insert_one({
    "listID": 1, 
    "listName": "list1", 
    "listDescription": "tempDescrip",
    "creationDate": "2024-10-27"})

# collection_list = db.list_collections()
# for c in collection_list:
#     print(c)
    

