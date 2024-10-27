from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import todo

class Item(BaseModel):
    name: str

app = FastAPI()

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
