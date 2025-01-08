import requests

if __name__ == '__main__':
    url = 'http://127.0.0.1:8000'
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

#    requests.get(url + '/shutdown')

