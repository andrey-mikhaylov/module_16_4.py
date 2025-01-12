import uvicorn
from fastapi import FastAPI, Path
from typing import Annotated


app = FastAPI()


# Создайте словарь
users = {'1': 'Имя: Example, возраст: 18'}


@app.get('/')
async def main_page() -> str:
    """ Главная страница """
    return "Главная страница"


# get запрос по маршруту '/users',
# который возвращает словарь users.
@app.get('/users')
async def get_users() -> dict[str, str]:
    """ Выдача всех пользователей """
    return users


# post запрос по маршруту '/user/{username}/{age}',
# который добавляет в словарь по максимальному по значению ключом значение строки
# "Имя: {username}, возраст: {age}".
# И возвращает строку "User <user_id> is registered".
@app.post('/user/{username}/{age}')
async def post_user(
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=24)]
    ) -> str:
    """ Добавление пользователя """
    user_id = str(int(max(users, key=int, default=0)) + 1)
    await put_user(user_id, username, age)
    return f"User {user_id} is registered"


# put запрос по маршруту '/user/{user_id}/{username}/{age}',
# который обновляет значение из словаря users под ключом user_id на строку
# "Имя: {username}, возраст: {age}".
# И возвращает строку "The user <user_id> is updated"
@app.put('/user/{user_id}/{username}/{age}')
async def put_user(
        user_id: Annotated[str, Path(min_length=1, max_length=3, description='Enter User ID', example='1')],
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=24)]
    ) -> str:
    """ Изменение пользователя """
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f"The user {user_id} is updated"


# delete запрос по маршруту '/user/{user_id}',
# который удаляет из словаря users по ключу user_id пару.
@app.delete('/user/{user_id}')
async def delete_user(
        user_id: Annotated[str, Path(min_length=1, max_length=3, description='Enter User ID', example='1')]
    ) -> str:
    """ Удаление пользователя """
    users.pop(user_id)
    return f'The user {user_id} is deleted'


@app.get('/shutdown')
async def shutdown():
    """ Выключение сервера """
    global server
    server.should_exit = True


@app.get('/restart')
async def restart():
    """ Перезапуск БД для теста """
    global users
    users = {'1': 'Имя: Example, возраст: 18'}


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