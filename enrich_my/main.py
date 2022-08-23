
from typing import Optional
from fastapi import FastAPI

from pydantic import BaseModel
from services.authmy import AuthServiceMy
from services.auth import AuthService
from services.apitesting import  get_auth_servicetesting, AuthServicetesting
from wait_for_pg import PGConnection
import requests

class Package(BaseModel):
    name: str
    number: str
    description: Optional[str] = None

app = FastAPI()

@app.get('/')
async def hello_world():
    return {'Hello' : 'World'}

@app.get('/user')
async def return_user_info_by_id(db_name, user_id):
    connection = PGConnection(db_name).main()
    user_info = AuthServiceMy(connection).get_by_id(user_id)
    return {'user_info' : user_info}

@app.get('/get_all_users_info_from_table')
async def return_user_info_by_id(db_name):
    connection = PGConnection(db_name).main()
    user_info = AuthServiceMy(connection).get_all_users_info_from_table()
    return {'user_info' : user_info}

@app.get('/test_async')
async def test_async():
    return AuthServicetesting.get_by_id()



# answer = requests.get("http://127.0.0.1:8000/user/", params={'db_name' : 'auth', 'user_id' : 'a61846cf-8882-4213-a471-f763000d1147'})
# print(f' eto answer : {answer}')
# @app.post("/package/{priority}")
# async def make_package(priority: int, package: Package, value: bool):
#     return {"priority": priority, **package.dict(), "value": value}