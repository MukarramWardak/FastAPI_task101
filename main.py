import openai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import yaml
from dotenv import load_dotenv
from tinydb import TinyDB, Query
import os
import json
from utils import get_user_params_and_roles,generate_answer,get_user_db,user_in_db

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

app = FastAPI()
load_dotenv()
user_db=get_user_db()
User=Query()

with open('users.json') as file:
    users=json.load(file)

class Chat(BaseModel):
    id:int
    tool:str
    message: str

@app.get("/")
async def root():
    return {"message": "Task 101"}

@app.get("/chatbot")
async def chatbot_info():
    return {"message": "Here to help you in every way. Kindly head over to chatbot for any kind of query!"}


@app.get("/users")
async def fetch_users():
    return user_in_db(user_db)


@app.post("/chatbot")
async def generated_responses(chat: Chat):
    try: 
        if user_db.search(User.user_id == chat.id):
            user_params= get_user_params_and_roles(chat.tool,chat.message)
        else:
            raise HTTPException(status_code=404,detail=f'User with id {chat.id} not found.')
    except HTTPException as e:
        raise e
    answer = generate_answer(chat.message, user_params)
    return {"response": answer}