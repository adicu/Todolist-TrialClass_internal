from fastapi import FastAPI, Request, HTTPException

from pydantic import BaseModel
from typing import Optional
import todo
from fastapi.middleware.cors import CORSMiddleware



class Task(BaseModel):
    taskID: int
    taskName: str
    taskDescription: str
    taskPriority: int
    taskStatus: bool
    completionDate: str
    creationDate: str
    parentID: int


class ListModel(BaseModel):
    listID: int
    listName: str
    listDescription: str
    creationDate: str

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

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

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

'''get all tasks'''
@app.get("/tasks")
def get_tasks():
    tasks = []
    for doc in todo.db.Tasks.find():
        doc["_id"] = str(doc["_id"])
        tasks.append(doc)
    return tasks

'''get task by id?'''
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    doc = todo.db.Tasks.find_one({"taskID": task_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Task not found")
    doc["_id"] = str(doc["_id"])
    return doc

'''create task'''
@app.post("/tasks", status_code=201)
def create_task(task: Task):
    result = todo.db.Tasks.insert_one(task.dict())
    new_task = todo.db.Tasks.find_one({"_id": result.inserted_id})
    new_task["_id"] = str(new_task["_id"])
    return new_task

#update
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    update_result = todo.db.Tasks.update_one({"taskID": task_id}, {"$set": task.dict()})
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    updated_task = todo.db.Tasks.find_one({"taskID": task_id})
    updated_task["_id"] = str(updated_task["_id"])
    return updated_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Delete a task by its taskID."""
    delete_result = todo.db.Tasks.delete_one({"taskID": task_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@app.get("/lists")
def get_lists():
    """Retrieve all lists."""
    lists = []
    for doc in todo.lists.find():
        doc["_id"] = str(doc["_id"])
        lists.append(doc)
    return lists

@app.get("/lists/{list_id}")
def get_list(list_id: int):
    """Retrieve a single list by its listID."""
    doc = todo.lists.find_one({"listID": list_id})
    if not doc:
        raise HTTPException(status_code=404, detail="List not found")
    doc["_id"] = str(doc["_id"])
    return doc

@app.post("/lists", status_code=201)
def create_list(list_item: ListModel):
    """Create a new list."""
    result = todo.lists.insert_one(list_item.dict())
    new_list = todo.lists.find_one({"_id": result.inserted_id})
    new_list["_id"] = str(new_list["_id"])
    return new_list

@app.put("/lists/{list_id}")
def update_list(list_id: int, list_item: ListModel):
    """Update an existing list by its listID."""
    update_result = todo.lists.update_one({"listID": list_id}, {"$set": list_item.dict()})
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="List not found")
    updated_list = todo.lists.find_one({"listID": list_id})
    updated_list["_id"] = str(updated_list["_id"])
    return updated_list

@app.delete("/lists/{list_id}")
def delete_list(list_id: int):
    """Delete a list by its listID."""
    delete_result = todo.lists.delete_one({"listID": list_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="List not found")
    return {"message": "List deleted successfully"}
