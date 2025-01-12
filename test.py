from requests import get, post, delete, put

url = 'http://127.0.0.1:8000'


def check(fn, path: str):
    result = fn(url + path).text
    print(fn.__name__, path, '->', result)


def test_ok():
    check(get,   '/users')
    check(post,  '/user/UrbanUser/24')
    check(post,  '/user/UrbanTest/36')
    check(post,  '/user/Admin/42')
    check(put,   '/user/1/UrbanProfi/28')
    check(delete,'/user/2')
    check(get,   '/users')
    check(delete,'/user/2')
    # Выдаёт
    # get /users -> []
    # post /user/UrbanUser/24 -> {"id":1,"username":"UrbanUser","age":24}
    # post /user/UrbanTest/36 -> {"id":2,"username":"UrbanTest","age":36}
    # post /user/Admin/42 -> {"id":3,"username":"Admin","age":42}
    # put /user/1/UrbanProfi/28 -> {"id":1,"username":"UrbanProfi","age":28}
    # delete /user/2 -> {"id":2,"username":"UrbanTest","age":36}
    # get /users -> [{"id":1,"username":"UrbanProfi","age":28},{"id":3,"username":"Admin","age":42}]
    # delete /user/2 -> {"detail":"User was not found"}

def test_error():
    check(get,    '/users1')
    check(post,   '/user/U/2224')
    check(delete, '/user/1111')
    check(delete, '/user/111')
    check(post,   '/user/Hi/99')
    # выдаёт
    # get /users1 -> {"detail":"Not Found"}
    # post /user/U/2224 -> {"detail":[{"type":"string_too_short","loc":["path","username"],"msg":"String should have at least 5 characters","input":"U","ctx":{"min_length":5}},{"type":"less_than_equal","loc":["path","age"],"msg":"Input should be less than or equal to 120","input":"2224","ctx":{"le":120}}]}
    # delete /user/1111 -> {"detail":[{"type":"less_than_equal","loc":["path","user_id"],"msg":"Input should be less than or equal to 100","input":"1111","ctx":{"le":100}}]}
    # delete /user/111 -> {"detail":[{"type":"less_than_equal","loc":["path","user_id"],"msg":"Input should be less than or equal to 100","input":"111","ctx":{"le":100}}]}
    # post /user/Hi/99 -> {"detail":[{"type":"string_too_short","loc":["path","username"],"msg":"String should have at least 5 characters","input":"Hi","ctx":{"min_length":5}}]}

if __name__ == '__main__':
    check(delete, '/users')
    print()
    test_ok()
    print()
    test_error()
    # requests.get(url + '/shutdown')

