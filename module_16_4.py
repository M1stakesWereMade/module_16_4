from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Создаем объект FastAPI
app = FastAPI()

# Инициализируем пустой список пользователей
users: List['User'] = []

# Модель User, которая будет хранить информацию о пользователе
class User(BaseModel):
    id: int
    username: str
    age: int

# GET запрос для получения всех пользователей
@app.get("/users", response_model=List[User])
def get_users():
    return users

# POST запрос для добавления нового пользователя
@app.post("/user/{username}/{age}", response_model=User)
def add_user(username: str, age: int):
    # Находим новый id для пользователя
    user_id = users[-1].id + 1 if users else 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

# PUT запрос для обновления данных пользователя
@app.put("/user/{user_id}/{username}/{age}", response_model=User)
def update_user(user_id: int, username: str, age: int):
    # Ищем пользователя по user_id
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    
    # Если пользователь не найден, выбрасываем ошибку 404
    raise HTTPException(status_code=404, detail="User was not found")

# DELETE запрос для удаления пользователя
@app.delete("/user/{user_id}", response_model=User)
def delete_user(user_id: int):
    # Ищем пользователя по user_id
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    
    # Если пользователь не найден, выбрасываем ошибку 404
    raise HTTPException(status_code=404, detail="User was not found")
