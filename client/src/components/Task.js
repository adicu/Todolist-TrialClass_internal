import React from "react";
import { useEffect, useState } from "react";
import "./task.css";

async function getSampleTask() {
    const response = await fetch('http://127.0.0.1:8000/task/read_sample?id=1', 
        {method: "GET"}
    );
    const data = await response.json();  // assuming the response is JSON
    console.log(data);
    return data
}

export default function Task() {
    // Put logic for hitting an endpoint to do CRUD stuff. 
    let tasks = new Array(5);
    let [task, setTask] = useState(null);


    useEffect(() => {
        async function fetchTask() {
            const taskData = await getSampleTask();
            setTask(taskData);
        }
        fetchTask();
    }, []);

    return (
        <div classname="task-box">
            <input type="text" placeholder="Enter Task Name" className="taskinput" />
            {JSON.stringify(task)}
        </div>
    );
}
