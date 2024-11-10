from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
import todo
from fastapi.middleware.cors import CORSMiddleware

class Item(BaseModel):
    name: str

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.delete("/task/deleteall")
async def deleteTask():
    todo.db.Tasks.delete_many({})

# Keep this commented out code if useful, otherwise remove. 
# async def createTask(request: Request):
#     req_json = request.json()
#     print(req_json)
#     todo.db.Tasks.insert_one(req_json)
#     return todo.db.collection.find_one({"taskID":{"$eq":id}})
# 
# @app.get("/task/read")
# async def readTask(id):
#     return todo.db.collection.find_one({"taskID":{"$eq":id}})

@app.get("/task/read_sample")
async def readTaskSample(id):
    return {
    "taskID": id, 
    "taskName": "Sample Task Name", 
    "taskDescription": "Sample Task Description", 
    "taskPriority": 1, 
    "taskStatus": False,
    "completionDate": "2024-10-31",
    "creationDate": "2024-10-27",
    "parentID": 1
    }

@app.post("/task/create")
async def createTask(id, name, desc, priority, status, compDate, createDate, parentID):
    todo.db.Tasks.insert_one({
        "taskID": id, 
        "taskName": name, 
        "taskDescription": desc, 
        "taskPriority": priority, 
        "taskStatus": status,
        "completionDate": compDate,
        "creationDate": createDate,
        "parentID": parentID})
    document = todo.db.Tasks.find_one({"taskID": id})
    if document:
        document["_id"] = str(document["_id"])
    return document

@app.get("/task/read")
async def readTask(id: int):
    document = todo.db.Tasks.find_one({"taskID": id})
    if document:
        document["_id"] = str(document["_id"])
    return document
