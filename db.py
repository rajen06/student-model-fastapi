from motor import motor_asyncio
from bson.objectid import ObjectId
from data_validation import (
    ErrorResponseModel
)


uri = "mongodb+srv://baghelraj45:no8twbvMeveO4Xw2@cluster0.3xse5mq.mongodb.net/?retryWrites=true&w=majority"
client = motor_asyncio.AsyncIOMotorClient(
    uri, tls=True, tlsAllowInvalidCertificates=True)
db = client.users
user_collection = db["users_collection"]


# Add User
async def add_user(user_data):
    try:
        user = await db.user_collection.insert_one(user_data)
        new_user = await db.user_collection.find_one({"_id": user.inserted_id})
        new_user["_id"] = str(new_user["_id"])
        return new_user
    except Exception as e:
        print("Exception in add_user:", e)
        return ErrorResponseModel(e, 500, "Internal Server Error")

# Retrieve user by id


async def get_user(id):
    try:
        user = await db.user_collection.find_one({"_id": ObjectId(id)})
        if user:
            user["_id"] = str(user["_id"])
            return user
    except Exception as e:
        print("Exception in get_user:", e)
        return ErrorResponseModel(e, 500, "Internal Server Error")

# Retrieve all users


async def get_all_user():
    try:
        users = []
        async for user in db.user_collection.find():
            user["_id"] = str(user["_id"])
            users.append(user)
        return users
    except Exception as e:
        print("Exception in get_all_user:", e)
        return ErrorResponseModel(e, 500, "Internal Server Error")


async def delete_user(id):
    try:
        user_info = await db.user_collection.find_one({"_id": ObjectId(id)})
        user_info["_id"] = str(user_info["_id"])
        print("user exist", user_info)
        print("id is", id)
        if user_info["_id"] == id:
            await db.user_collection.delete_one({"_id": ObjectId(id)})
            return True
        else:
            return False
    except Exception as e:
        print("Exception in get_all_user:", e)
        return ErrorResponseModel(e, 500, "Internal Server Error")


async def update_user(id: str, data: dict):
    try:
        print("data is", data, len(data))
        if len(data) < 1:
            return False
        user_info = await db.user_collection.find_one({"_id": ObjectId(id)})
        user_info["_id"] = str(user_info["_id"])
        if user_info["_id"] == id:
            update_user_info = await db.user_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
            print("user update info", update_user_info)
            if update_user_info:
                return True
            return False
    except Exception as e:
        print("Exception in get_all_user:", e)
        return ErrorResponseModel(e, 500, "Internal Server Error")
