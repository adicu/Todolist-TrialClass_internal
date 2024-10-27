from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import todo

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
    return todo.db.collection.find({"taskID":{"$eq":id}})

@app.get("/task/read")
async def readTask(id):
    return todo.db.collection.find({"taskID":{"$eq":id}})
