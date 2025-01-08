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
2024/02/18 00:00|Домашнее задание по теме "CRUD Запросы: Get, Post, Put Delete."
Цель: выработать навык работы с CRUD запросами.

Задача "Имитация работы с БД":
Создайте новое приложение FastAPI и сделайте CRUD запросы.
Создайте словарь users = {'1': 'Имя: Example, возраст: 18'}
Реализуйте 4 CRUD запроса:
get запрос по маршруту '/users', который возвращает словарь users.
post запрос по маршруту '/user/{username}/{age}', который добавляет в словарь по максимальному по значению ключом значение строки "Имя: {username}, возраст: {age}". И возвращает строку "User <user_id> is registered".
put запрос по маршруту '/user/{user_id}/{username}/{age}', который обновляет значение из словаря users под ключом user_id на строку "Имя: {username}, возраст: {age}". И возвращает строку "The user <user_id> is updated"
delete запрос по маршруту '/user/{user_id}', который удаляет из словаря users по ключу user_id пару.
Выполните каждый из этих запросов по порядку. Ответы должны совпадать:
1. GET '/users'
{
"1": "Имя: Example, возраст: 18"
}
2. POST '/user/{username}/{age}' # username - UrbanUser, age - 24
"User 2 is registered"
3. POST '/user/{username}/{age}' # username - NewUser, age - 22
"User 3 is registered"
4. PUT '/user/{user_id}/{username}/{age}' # user_id - 1, username - UrbanProfi, age - 28
"User 1 has been updated"
5. DELETE '/user/{user_id}' # user_id - 2
"User 2 has been deleted"
6. GET '/users'
{
"1": "Имя: UrbanProfi, возраст: 28",
"3": "Имя: NewUser, возраст: 22"
}
Пример результата выполнения программы:
Как должен выглядеть Swagger:


Примечания:
Не забудьте написать валидацию для каждого запроса, аналогично предыдущему заданию.
Файл module_16_3.py загрузите на ваш GitHub репозиторий. В решении пришлите ссылку на него.
"""