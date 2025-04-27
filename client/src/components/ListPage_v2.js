/*
* Meant to connect with server
*/

import {useEffect, useState} from 'react';
import {useParams} from 'react-router-dom';

import NavBar from "./NavBar";
import AddForm from "./AddForm";
import Task from "./Task";


export default function ListPage() {
    // parameters
    const {activeListId} = useParams() // get id of active list from URL

    // states
    const [lists, setLists] = useState([])
    const [tasks, setTasks] = useState([])

    // effects
    useEffect(() => {
        async function fetchLists() {
            try {
                const response = await fetch("https://localhost:8000/lists",
                    {method: "GET"}
                )
                const data = await response.json(); // expecting list of objects
                setLists(data)
    
                // FIX: make sure we get lists in list form
                // FIX: make sure lists starts with {"0", All}, id's increment by 1 (for navbar)
            }
            catch (error) {
                console.error("There was an error fetching the lists:", error)
            }
        }
        async function fetchTasks() {
            try {
                const response = await fetch(`https://localhost:8000/task/read_tasks?${activeListId}`,
                    {method: "GET"}
                )
                const data = await response.json() // expecting list of objects
                setTasks(data)
    
                // FIX: make sure we get tasks in list form
            }
            catch (error) {
                console.error("There was an error fetching the lists:", error)
            }
        }
        fetchTasks()
        fetchLists()
    }, [activeListId]) // whenever we change active list (change pages), we re-fetch relevant data

    // event handlers (as asyn functions)
    async function handleListAdd(name) {
        try {
            const response = await fetch(`https://localhost:8000/list/create`,
                {method: "POST", body: JSON.stringify({name: name})}
            )
            const data = await response.json() // expecting updated lists
            setLists(data)

            // FIX: make sure to create list id, add as {id: uuid, name: name}, return lists
        }
        catch (error) {
            console.error("There was an error adding the list:", error)
        }
    }
    async function handleListDelete(id) {
        try {
            const response = await fetch(`https://localhost:8000/list/delete`,
                {method: "POST", body: JSON.stringify({id: id})}
            )
            const data = await response.json() // expecting updated lists
            setLists(data)

            // FIX: make sure to delete list w/ id (and all relevant tasks), return lists
        }
        catch (error) {
            console.error("There was an error deleting the list:", error)
        }
    }
    async function handleTaskCheck(id) {
        try {
            const response = await fetch(`https://localhost:8000/task/check`,
                {method: "POST", body: JSON.stringify({id: id})}
            )
            const data = await response.json() // expecting updated tasks
            setTasks(data)

            // FIX: make sure to find task w/ id and set completion as opposite 
        }
        catch (error) {
            console.error("There was an error updating the task:", error)
        }
    }
    async function handleTaskDelete(id) {
        try {
            const response = await fetch(`https://localhost:8000/task/delete`,
                {method: "POST", body: JSON.stringify({id: id})}
            )
            const data = await response.json() // expecting updated tasks
            setTasks(data)

            // FIX: make sure to find task w/ id and delete it, return tasks
        }
        catch (error) {
            console.error("There was an error deleting the task:", error)
        }
    }
    async function handleTaskAdd(listId, name, priority, description) {
        try {
            const response = await fetch(`https://localhost:8000/task/delete`,
                {method: "POST",
                body: JSON.stringify({listId: listId, name: name, priority: priority, description: description})}
            )
            const data = await response.json() // expecting updated tasks
            setTasks(data)

            // FIX: make sure to create new task id, add task like the following, return tasks
            // {id: 300, listId: listId, list: get using listId, name: name, description: description, priority: priority, completion: false}
        }
        catch (error) {
            console.error("There was an error adding the task:", error)
        }
    }

    // other variables
    const isValidListSelected = (lists.map(l => "" + l.listId).includes(activeListId))
    const activeListName = (lists.map(l => "" + l.id).includes(activeListId)) ? lists[activeListId].name : ""

    // <ListPage/> component:
    return (
        <>
        <h1>My To Dos</h1>
        <div className="container-fluid">
            <div className="row">
                <div className="col-sm-2">
                    <NavBar handleAdd={handleListAdd} handleDelete={handleListDelete} lists={lists}/>
                </div>

                <div className="col-sm-10">
                {
                isValidListSelected ?
                    <>
                    <h3 className="text-center">Tasks for {activeListName}</h3>
                    <div className="row d-flex justify-content-center">
                        <div className="col-sm-10">
                            <AddForm lists={lists} handleAdd={handleTaskAdd}/>
                            <hr/>
                            {
                            tasks.map(task => {
                            return <>
                            <Task {...task} handleCheck={handleTaskCheck} handleDelete={handleTaskDelete}/>
                            <br/>
                            </>
                            })
                            }
                        </div>
                    </div>
                    </>
                :
                    <div className="row d-flex justify-content-center">
                        No list selected. Please select a list.
                    </div>
                }
                </div>
            </div>
        </div>
        </>
    )
}