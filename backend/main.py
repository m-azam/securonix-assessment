from fastapi import FastAPI, Header, Body
import sqlite3
import hashlib
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import plotly.graph_objects as go
import itertools
import statistics

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
    db_connection.close()
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
        db_connection.close()
        return json.dumps([dict(iterator) for iterator in rows])

@app.post("/submit")
async def login(request: dict = Body(...), username: str = Header(None), password: str = Header(None)):
    if (is_valid_user(username, password)):
        db_connection = sqlite3.connect('sqnx-db.db')
        db_cursor = db_connection.cursor()
        attempt = 1
        last_attempt = db_cursor.execute("SELECT MAX(surveyAttemptNumber) FROM Responses").fetchall()[0][0]
        if (last_attempt is not None):
            attempt = last_attempt + 1
        for key, value in request.items():
            db_cursor.execute("INSERT INTO Responses VALUES (?, ?, ?, ?)", (int(value), username, int(key), attempt))
            db_connection.commit()
        db_connection.close()

def plot_category_average(attempt, username):
    db_connection = sqlite3.connect('sqnx-db.db')
    db_cursor = db_connection.cursor()
    average = db_cursor.execute("SELECT AVG(questionResponse) FROM Responses WHERE username = (?) AND surveyAttemptNumber = (?)", (username, attempt)).fetchall()[0][0]
    db_connection.close()
    labels = ['Overall Average']
    values = [average]
    fig = go.Figure(data=[go.Bar(x=labels, y=values, text=values)])
    fig.update_yaxes(range=list([0,100]))
    fig.update_traces(width=0.35)
    fig.show()
    fig.write_image("generated_graph/average_overall.png")

def get_question_id(category, subcategory = None):
    db_connection = sqlite3.connect('sqnx-db.db')
    db_cursor = db_connection.cursor()
    questionIdList = []
    if (subcategory == None):
        questionIdList = list(itertools.chain(*db_cursor.execute("SELECT questionId FROM Questions WHERE questionCategory = (?)", [category]).fetchall()))
    else:
        questionIdList = list(itertools.chain(*db_cursor.execute("SELECT questionId FROM Questions WHERE questionCategory = (?) AND questionSub = (?)", (category, subcategory)).fetchall()))
    db_connection.close()
    return questionIdList

def plot_category_average(category, attempt, username):
    db_connection = sqlite3.connect('sqnx-db.db')
    db_cursor = db_connection.cursor()
    questionIdList = get_question_id(category)
    query = "SELECT questionResponse FROM Responses WHERE username = (?) AND surveyAttemptNumber = (?) AND questionId IN ({sequence})".format(sequence=','.join(str(i) for i in questionIdList))
    responses_tuple = db_cursor.execute(query, (username, attempt)).fetchall()
    response_list = list(itertools.chain(*responses_tuple))
    db_connection.close()
    average = statistics.mean(response_list)
    labels = [category]
    values = [round(average,2)]
    fig = go.Figure(data=[go.Bar(x=labels, y=values, text=values)])
    fig.update_yaxes(range=list([0,100]))
    fig.update_traces(width=0.35)
    fig.write_image("generated_graph/average_"+ category +".png")

def plot_sub_category_average(category, attempt, username):
    labels = []
    values = []
    db_connection = sqlite3.connect('sqnx-db.db')
    db_cursor = db_connection.cursor()
    questionIdList = get_question_id(category, "Define")
    query = "SELECT questionResponse FROM Responses WHERE username = (?) AND surveyAttemptNumber = (?) AND questionId IN ({sequence})".format(sequence=','.join(str(i) for i in questionIdList))
    responses_tuple = db_cursor.execute(query, (username, attempt)).fetchall()
    response_list = list(itertools.chain(*responses_tuple))
    average = statistics.mean(response_list)
    labels.append("Define")
    values.append(round(average,2))

    questionIdList = get_question_id(category, "Manage")
    query = "SELECT questionResponse FROM Responses WHERE username = (?) AND surveyAttemptNumber = (?) AND questionId IN ({sequence})".format(sequence=','.join(str(i) for i in questionIdList))
    responses_tuple = db_cursor.execute(query, (username, attempt)).fetchall()
    response_list = list(itertools.chain(*responses_tuple))
    average = statistics.mean(response_list)
    labels.append("Manage")
    values.append(round(average,2))

    questionIdList = get_question_id(category, "Use")
    query = "SELECT questionResponse FROM Responses WHERE username = (?) AND surveyAttemptNumber = (?) AND questionId IN ({sequence})".format(sequence=','.join(str(i) for i in questionIdList))
    responses_tuple = db_cursor.execute(query, (username, attempt)).fetchall()
    response_list = list(itertools.chain(*responses_tuple))
    average = statistics.mean(response_list)
    labels.append("Use")
    values.append(round(average,2))

    fig = go.Figure(data=[go.Bar(x=labels, y=values, text=values)])
    fig.update_yaxes(range=list([0,100]))
    fig.update_traces(width=0.35)
    fig.write_image("generated_graph/sub_cat_average_for_"+ category +".png")