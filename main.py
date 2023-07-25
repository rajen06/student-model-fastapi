from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from db import (
    add_user,
    get_user,
    get_all_user,
    delete_user,
    update_user
)

from data_validation import (
    UserCreateSchema,
    UserUpdateSchema,
    ResponseModel,
    ErrorResponseModel
)


app = FastAPI()


@app.post("/user", response_description="User data added into the database")
async def add_user_data(user_data: UserCreateSchema):
    try:
        user_info = jsonable_encoder(user_data)
        resp = await add_user(user_info)
        return ResponseModel(resp, "User added successfuly")
    except Exception as e:
        print("Exception in add_user_data:", e)
        return ErrorResponseModel(e, 500, "Internal Server Error")


@app.get("/user/{user_id}", response_description="User retrieved")
async def get_user_data(user_id: str):
    try:
        user_info = await get_user(user_id)
        if user_info["_id"]:
            return ResponseModel(user_info, "User info retrieved successfully")
        elif user_info["error"]:
            return ErrorResponseModel(str(user_info["error"]), user_info["statusCode"], user_info["message"])
        else:
            return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")
    except Exception as e:
        print("Exception in get_user_data:", e)
        return ErrorResponseModel(e, 500, "Internal Server Error")


@app.get("/users", response_description="Users retrieved")
async def get_all_users_data():
    try:
        users_info = await get_all_user()
        if len(users_info) > 0:
            return ResponseModel(users_info, "All users info retrieved successfully")
        elif users_info["error"]:
            return ErrorResponseModel(str(users_info["error"]), users_info["statusCode"], users_info["message"])
        else:
            return ResponseModel(users_info, "Empty list retrieved")
    except Exception as e:
        print("Exception in get_all_users_data:", e)
        return ErrorResponseModel(e, 500, "Internal Server Error")


@app.delete("/user/{user_id}", response_description="User deleted")
async def delete_user_data(user_id: str):
    try:
        deleted_user = await delete_user(user_id)
        print("deleted user", deleted_user)
        if deleted_user == True:
            return ResponseModel("User with ID: {} removed".format(user_id), "User deleted successfully")
        elif deleted_user["error"]:
            return ErrorResponseModel(str(deleted_user["error"]), deleted_user["statusCode"], deleted_user["message"])
        else:
            return ErrorResponseModel(
                "An error occurred", 404, "user with id {0} doesn't exist".format(user_id))

    except Exception as e:
        print("Exception in get_all_users_data:", e)
        return ErrorResponseModel(e, 500, "Internal Server Error")


@app.put("/user/{user_id}")
async def update_user_data(user_id: str, user_data: UserUpdateSchema):
    try:
        user_data = {k: v for k, v in user_data.dict().items()
                     if v is not None}
        print(user_data)
        updated_user = await update_user(user_id, user_data)
        if updated_user == True:
            return ResponseModel("User with ID: {} name update is successful".format(user_id),
                                 "User name updated successfully")
        elif updated_user["error"]:
            return ErrorResponseModel(str(updated_user["error"]), updated_user["statusCode"], updated_user["message"])
        else:
            return ErrorResponseModel(
                "An error occurred", 404, "user with id {0} doesn't exist".format(user_id))
    except Exception as e:
        print("Exception in update_user_data:", e)
        return ErrorResponseModel(e, 500, "Internal Server Error")
