import requests
from zope.interface import Invalid

url = 'http://127.0.0.1:8000'


def test_ok():
    print(requests.get      (url + '/users').text)
    print(requests.post     (url + '/user/UrbanUser/24').text)
    print(requests.post     (url + '/user/NewUser/22').text)
    print(requests.put      (url + '/user/1/UrbanProfi/28').text)
    print(requests.delete   (url + '/user/2').text)
    print(requests.get      (url + '/users').text)
    # Выдаёт
    # {"1":"Имя: Example, возраст: 18"}
    # "User 2 is registered"
    # "User 3 is registered"
    # "The user 1 is updated"
    # "The user 2 is deleted"
    # {"1":"Имя: UrbanProfi, возраст: 28","3":"Имя: NewUser, возраст: 22"}


def test_error():
    print(requests.get      (url + '/users1').text)
    print(requests.post     (url + '/user/U/2224').text)
    print(requests.delete   (url + '/user/1111').text)
    print(requests.delete   (url + '/user/111').text)


if __name__ == '__main__':
    requests.get(url + '/restart')
    test_ok()
    print()
    test_error()
    # requests.get(url + '/shutdown')

