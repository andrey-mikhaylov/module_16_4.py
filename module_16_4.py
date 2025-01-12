import uvicorn
from fastapi import FastAPI, Path, HTTPException
from typing import List, Annotated
from pydantic import BaseModel, Field


app = FastAPI()


MAX_USER_ID = 100
MAX_AGE = 120

id_field       = Field(..., ge=1, le=MAX_USER_ID,          description='номер пользователя',   example=1)
username_field = Field(..., min_length=5, max_length=20,   description='имя пользователя',     example='UrbanUser')
age_field      = Field(..., ge=18, le=MAX_AGE,             description='возраст пользователя', example=24)

class User(BaseModel):
    id: int = id_field
    username: str = username_field
    age: int = age_field

users: List[User] = []


@app.get('/')
async def main_page() -> str:
    """ Главная страница """
    return "Главная страница"


@app.get('/users', response_model=List[User])
async def get_users() -> List[User]:
    """ Выдача всех пользователей

    get запрос по маршруту '/users'

    Возвращает список users.
    """
    return users


@app.post('/user/{username}/{age}', response_model=User)
async def post_user(
        username: Annotated[str, username_field],
        age: Annotated[int, age_field]
    ) -> User:
    """ Добавление пользователя

    post запрос по маршруту '/user/{username}/{age}'

    Добавляет в список users объект User.
    id этого объекта будет на 1 больше, чем у последнего в списке users. (нет)
    Если список users пустой, то 1.
    Все остальные параметры объекта User - переданные в функцию username и age соответственно.
    В конце возвращает созданного пользователя.
    """
    new_id = max([user.id for user in users], default = 0) + 1
    user = User(id=new_id, username=username, age=age)
    users.append(user)
    return user


def __get_user_index(user_id: int) -> int | None:
    index = [index for index, user in enumerate(users) if user.id == user_id]
    if len(index) != 1:
        return None
    return index[0]


@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def put_user(
        user_id: Annotated[int, id_field],
        username: Annotated[str, username_field],
        age: Annotated[int, age_field]
    ) -> User:
    """ Изменение пользователя

    put запрос по маршруту '/user/{user_id}/{username}/{age}'

    Обновляет username и age пользователя, если пользователь с таким user_id есть в списке users
    и возвращает его.
    В случае отсутствия пользователя выбрасывается
    исключение HTTPException с описанием "User was not found" и кодом 404.
    """
    index = __get_user_index(user_id)
    if index is None:
        raise HTTPException(status_code=404, detail="User was not found")

    user = User(id=user_id, username=username, age=age)
    users[index] = user
    return user


@app.delete('/user/{user_id}', response_model=User)
async def delete_user(user_id: Annotated[int, id_field]) -> User:
    """ Удаление пользователя

    delete запрос по маршруту '/user/{user_id}'

    Удаляет пользователя, если пользователь с таким user_id есть в списке users и возвращает его.
    В случае отсутствия пользователя выбрасывается исключение HTTPException с описанием "User was not found" и кодом 404.
    """
    index = __get_user_index(user_id)
    if index is None:
        raise HTTPException(status_code=404, detail="User was not found")

    user = users.pop(index)
    return user


@app.delete('/users')
async def clear() -> List[User]:
    """ Очистка БД для теста """
    users.clear()
    return users


@app.get('/shutdown')
async def shutdown():
    """ Выключение сервера """
    global server
    server.should_exit = True


if __name__ == '__main__':
    server = uvicorn.Server(uvicorn.Config(app=app))
    server.run()


"""
2024/02/19 00:00|Домашнее задание по теме "Модели данных Pydantic"
Если вы решали старую версию задачи, проверка будет производиться по ней.
Ссылка на старую версию тут.

Цель: научиться описывать и использовать Pydantic модель.

Задача "Модель пользователя":
Подготовка:
Используйте CRUD запросы из предыдущей задачи.
Создайте пустой список users = []
Создайте класс(модель) User, наследованный от BaseModel, который будет содержать следующие поля:
id - номер пользователя (int)
username - имя пользователя (str)
age - возраст пользователя (int)

Измените и дополните ранее описанные 4 CRUD запроса:

get запрос по маршруту '/users' теперь возвращает список users.

post запрос по маршруту '/user/{username}/{age}', теперь:
Добавляет в список users объект User.
id этого объекта будет на 1 больше, чем у последнего в списке users. Если список users пустой, то 1.
Все остальные параметры объекта User - переданные в функцию username и age соответственно.
В конце возвращает созданного пользователя.

put запрос по маршруту '/user/{user_id}/{username}/{age}' теперь:
Обновляет username и age пользователя, если пользователь с таким user_id есть в списке users и возвращает его.
В случае отсутствия пользователя выбрасывается исключение HTTPException с описанием "User was not found" и кодом 404.

delete запрос по маршруту '/user/{user_id}', теперь:
Удаляет пользователя, если пользователь с таким user_id есть в списке users и возвращает его.
В случае отсутствия пользователя выбрасывается исключение HTTPException с описанием "User was not found" и кодом 404.

Выполните каждый из этих запросов по порядку. Ответы должны совпадать:
1. GET '/users'
[]
2. POST '/user/{username}/{age}' # username - UrbanUser, age - 24

3. POST '/user/{username}/{age}' # username - UrbanTest, age - 36

4. POST '/user/{username}/{age}' # username - Admin, age - 42

5. PUT '/user/{user_id}/{username}/{age}' # user_id - 1, username - UrbanProfi, age - 28

6. DELETE '/user/{user_id}' # user_id - 2

7. GET '/users'

8. DELETE '/user/{user_id}' # user_id - 2

Файл module_16_4.py загрузите на ваш GitHub репозиторий. В решении пришлите ссылку на него.
"""