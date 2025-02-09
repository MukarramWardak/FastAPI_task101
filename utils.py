import json
import os
import openai
from openai import OpenAI
import yaml
from fastapi import HTTPException
from tinydb import TinyDB,Query

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)
db=TinyDB('db.json')
user_db=TinyDB('users.json')
User = Query()

def get_user_db():
    return user_db

def get_db():
    return db

def load_config(file_path):
    with open(file_path,'r') as file:
        return yaml.safe_load(file)
    
config=load_config('config.yaml')
tools=config['openai_tool']

with open('users.json') as file:
    users=json.load(file)

def get_user_params_and_roles(tool:str,input_text:str):
        if  tool in tools:
            user_params = tools[tool]
            tools[tool]['messages'][1]['content']=input_text
            return user_params
        else:
            raise HTTPException(status_code=404, detail="No Such tool amigo! try : tool1, tool2 or tool3.")
        
    
def generate_answer(input_text:str , user_params: dict):
    completion = client.chat.completions.create(
        **user_params
    )
    reply_dict = completion.to_dict()
    reply=reply_dict['choices'][0]['message']['content']
    db.insert({input_text: reply})
    return reply

def user_in_db(db):
    lst=[]
    for x in db:
        lst.append(x)
    return lst