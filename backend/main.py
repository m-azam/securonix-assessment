from fastapi import FastAPI, Header, Body
import sqlite3
import hashlib
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()


app = FastAPI()

origins = ["http://0.0.0.0:8900"]
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AuthRequest(BaseModel):
    username: str
    password: str

def is_valid_user(request_username, request_password):
    db_connection = sqlite3.connect('sqnx-db.db')
    db_cursor = db_connection.cursor()
    stored_hash = db_cursor.execute("SELECT password FROM User WHERE username = ?", [request_username]).fetchall()
    if (hashlib.sha256(request_password.encode('utf-8')).hexdigest() == stored_hash[0][0]):
        return True
    else:
        return False

@app.post("/login")
async def login(request: AuthRequest, username: str = Header(None), password: str = Header(None)):
    if (is_valid_user(username, password)):
        return request.username
    else:
        return "Invalid user"

@app.post("/questions")
async def fetch_questions(request: AuthRequest):
    if (is_valid_user(request.username, request.password)):
        db_connection = sqlite3.connect('sqnx-db.db')
        db_connection.row_factory = sqlite3.Row
        db_cursor = db_connection.cursor()
        rows = db_cursor.execute("SELECT * FROM Questions").fetchall()
        return json.dumps([dict(iterator) for iterator in rows])

@app.post("/questions")
async def fetch_questions(request: AuthRequest):
    if (is_valid_user(request.username, request.password)):
        db_connection = sqlite3.connect('sqnx-db.db')
        db_connection.row_factory = sqlite3.Row
        db_cursor = db_connection.cursor()
        rows = db_cursor.execute("SELECT * FROM Questions").fetchall()
        return json.dumps([dict(iterator) for iterator in rows])

@app.post("/submit")
async def login(request: dict = Body(...), username: str = Header(None), password: str = Header(None), number_of_questions: int = Header(None)):
    if (is_valid_user(username, password)):
