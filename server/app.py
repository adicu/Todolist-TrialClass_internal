from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
import time
import todo  # your module where `db = MongoClient(...)[...]`

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

class Task(BaseModel):
    taskID: int = 0
    taskName: str
    taskDescription: str = ""
    taskPriority: int = 0
    taskStatus: bool: False
    completionDate: str = ""
    creationDate: str = ""
    listID: int = 0

class ListModel(BaseModel):
    listID: int = 0
    listName: str
    listDescription: str = ""
    creationDate: str = ""

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.delete("/tasks")
async def delete_all_tasks():
    result = todo.db.Tasks.delete_many({})
    return {"deleted_count": result.deleted_count}

@app.get("/tasks", response_model=list[Task])
async def get_tasks():
    docs = []
    for doc in todo.db.Tasks.find():
        doc["_id"] = str(doc["_id"])
        docs.append(doc)
    return docs

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    doc = todo.db.Tasks.find_one({"taskID": task_id})
    if not doc:
        raise HTTPException(404, "Task not found")
    doc["_id"] = str(doc["_id"])
    return doc

@app.post("/task/create")
async def create_task(task: Task):
    task_id = int(time.time() * 1000)
    new_task = {
        "taskID": task_id,
        "taskName": task.name,
        "taskDescription": task.desc,
        "taskPriority": task.priority,
        "taskStatus": False,
        "completionDate": task.compDate,
        "creationDate": str(datetime.date.today()),
    }
    print(new_task)
    todo.db.Tasks.insert_one(new_task)
    return str(new_task)

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    res = todo.db.Tasks.update_one({"taskID": task_id}, {"$set": task.dict()})
    if res.matched_count == 0:
        raise HTTPException(404, "Task not found")
    return task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    res = todo.db.Tasks.delete_one({"taskID": task_id})
    if res.deleted_count == 0:
        raise HTTPException(404, "Task not found")
    return {"message": "Task deleted"}

# ---- Lists ----

@app.get("/lists", response_model=list[ListModel])
async def get_lists():
    docs = []
    for doc in todo.db.Lists.find():
        doc["_id"] = str(doc["_id"])
        docs.append(doc)
    return docs

@app.get("/lists/{list_id}", response_model=ListModel)
async def get_list(list_id: int):
    doc = todo.db.Lists.find_one({"listID": list_id})
    if not doc:
        raise HTTPException(404, "List not found")
    doc["_id"] = str(doc["_id"])
    return doc

@app.post("/list/create", status_code=201, response_model=ListModel)
async def create_list(list_item: ListModel):
    new_list = {
        "listID": int(time.time() * 1000),
        "listName": list_item.listName,
        "listDescription": "",
        "creationDate": str(datetime.date.today()),
    }
    todo.db.Lists.insert_one(new_list)
    return new_list

@app.put("/lists/{list_id}", response_model=ListModel)
async def update_list(list_id: int, list_item: ListModel):
    res = todo.db.Lists.update_one({"listID": list_id}, {"$set": list_item.dict()})
    if res.matched_count == 0:
        raise HTTPException(404, "List not found")
    return list_item

@app.delete("/lists/{list_id}")
async def delete_list(list_id: int):
    res = todo.db.Lists.delete_many({"listID": list_id})
    if res.deleted_count == 0:
        raise HTTPException(404, "List not found")
    return {"message": "List deleted"}
