from fastapi import FastAPI, Request
import todo
from fastapi.middleware.cors import CORSMiddleware

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

@app.post("/task/create")
async def createTask(request: Request):
    req_json = request.json()
    print(req_json)
    todo.db.Tasks.insert_one(req_json)
    return todo.db.collection.find_one({"taskID":{"$eq":id}})

@app.get("/task/read")
async def readTask(id):
    return todo.db.collection.find_one({"taskID":{"$eq":id}})

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
