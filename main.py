from fastapi import FastAPI
from entities.task import Task
from entities.user import User

import database

app = FastAPI(title="Python API", version="1.0.0")

database.initialize_database()

@app.get("/tasks", response_model=list[Task])
def get_tasks():
    connection = database.connect()
    try:
        with connection:
            
            dbresult = connection.execute(
                "SELECT title, description FROM tasks"
            )
            tasks = [
                Task(title=row[0], description=row[1])
                for row in dbresult.fetchall()
            ]
            return tasks
    finally:
        connection.close()

@app.post("/tasks")
def create_task(payload: Task):
    connection = database.connect()
    try:
        with connection:
            connection.execute(
                "INSERT INTO tasks (title, description) VALUES (?, ?)",
                (payload.title, payload.description),
            )
    finally:
        connection.close()
    return "All done"

@app.post("/users")
def create_user(payload: User):
    connection = database.connect()
    try:
        with connection:
            connection.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (payload.username, payload.password),
            )
    finally:
        connection.close()
    return "All done"

@app.get("/users", response_model=list[User])
def get_users():
    connection = database.connect()
    try:
        with connection:
            
            dbresult = connection.execute(
                "SELECT username, password FROM users"
            )
            users = [
                User(username=row[0], password=row[1])
                for row in dbresult.fetchall()
            ]
            return users
    finally:
        connection.close()