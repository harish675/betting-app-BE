
from ...curd.curd import DBOperation
from .models import User
from fastapi import HTTPException
from .entities import IUser
from .utility import (get_hashed_password)


class UserService:
    def __init__(self):
        self.db_operations = DBOperation()
        self.table = User

    def create_user(self, payload ,session)-> IUser:
         #check user exists
         user_details = self.db_operations.read(table=self.table,query=User.email==payload["email"],session=session)
         if user_details:
             raise HTTPException(status_code=409, detail="User email already exists")
         username_details = self.db_operations.read(table=self.table,query=User.username==payload["username"],session=session)
         if username_details:
             raise HTTPException(status_code=409, detail="Username already exists")
         
         mobile_number = self.db_operations.read(table=self.table,query=User.mobile_number==payload["mobile_number"],session=session)
         if mobile_number:
             raise HTTPException(status_code=409, detail="Mobile number already exists")
         
         if payload["password"] != payload["confirm_password"]:
             raise HTTPException(status_code=400, detail="Password and confirm password do not match")
         
         #  prepare data for user creation
         hashed_password = get_hashed_password(payload["password"])
         payload["password"] = hashed_password
         doc = User(**payload)
         user = self.db_operations.create(data=doc,session=session)
         if not user:
                raise HTTPException(status_code=500, detail="User creation failed.")
         return user
         
