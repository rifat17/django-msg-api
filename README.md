**Steps**

1. unzip
2. cd in extracted directory
3.      `python -m venv .venv`
4.      `pip install -r requirements.txt`
5. cd into project
6.      `python manage.py test apps`
7.      `python manage.py runserver`


**APIs**
- Register: http://127.0.0.1:8000/api/auth/register/ (POST)
>payload
```
{
    "username": "hasib",
    "email": "hasib@mail.com",
    "password": "123456",
    "confirm_password": "123456"
}
```

- Login: http://127.0.0.1:8000/api/auth/login/ (POST)

> payload
```
{
    "username": "hasib",
    "password": "123456"
}
```

> please copy the token, required in next api

- Create a message: http://127.0.0.1:8000/api/messages/ (POST)
> set header  `Authorization: Token ede41608a206c5ef5f9eb56670ae5f9201b0f515`

> payload
```
{
    "message" : "your message here"
}
```

> curl example

 ```
 curl --location --request POST 'http://127.0.0.1:8000/api/messages/' \
--header 'Authorization: Token ede41608a206c5ef5f9eb56670ae5f9201b0f515' \
--form 'message="msg"'

 ```
