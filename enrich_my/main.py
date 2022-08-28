
from typing import Optional
from fastapi import FastAPI , APIRouter, Depends

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


router = APIRouter()
@router.get('/')
async def get_hw(
        apitest_service: AuthServicetesting = Depends(get_auth_servicetesting),
):
    dashboards = await apitest_service.get_by_id()
    return dashboards

# async def test_async():
#     return AuthServicetesting.get_by_id()


app.include_router(router, prefix='/test_async')

# @app.get('/get_all_users_info_from_table_async')
# async def return_user_info_by_id_async(db_name, user_id):
#     connection = PGConnection(db_name).main()
#     user_info = AuthService(connection).get_by_id(user_id)
#     return {'user_info' : user_info}


# answer = requests.get("http://127.0.0.1:8000/user/", params={'db_name' : 'auth', 'user_id' : 'a61846cf-8882-4213-a471-f763000d1147'})
# print(f' eto answer : {answer}')
# @app.post("/package/{priority}")
# async def make_package(priority: int, package: Package, value: bool):
#     return {"priority": priority, **package.dict(), "value": value}