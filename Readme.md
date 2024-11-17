## Setup

### Requirements:
1. python3(min version 3.13)
2. mysql(min version 8.4)

### Steps
1. clone the repo
2. create a new python3 virtualenv using command **python -m venv venv**
3. activate venv using command **source venv/bin/activate**
4. install dependencies using command **pip install -r requirements.txt**
5. configure databse creds in glamy_ai.settings file(mysql min version 8.4)
6. run migrations on database using command **python manage.py migrate**
7. run application using command **python manage.py runserver**
8. test health of application **curl --location 'http://127.0.0.1:8000/health'**



### API Samples
#### generate otp for signup or login
```bash
curl --location 'http://127.0.0.1:8000/api/users/send-otp/' \
--header 'Content-Type: application/json' \
--data '{
    "mobile": "1234567890"
}'
```

#### verify otp for signup or login
##### if user already exists(login)
```bash
curl --location 'http://127.0.0.1:8000/api/users/verify-otp/' \
--header 'Content-Type: application/json' \
--data '{
    "mobile": "1234567890",
    "otp": "376570"
}'
```
##### if new user(signup)
```bash
curl --location 'http://127.0.0.1:8000/api/users/verify-otp/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "mobile": "1234567890",
    "otp": "255935",
    "first_name": "Sagar",
    "last_name": "Yadav",
    "email": "sagar@gmail.com"
}'
```

#### refresh access token using refresh token
```bash
curl --location --request GET 'http://127.0.0.1:8000/api/users/token/refresh/' \
--header 'Content-Type: application/json' \
--data '{
    "refresh": "<refrsh_token>"
}'
```

#### sample api for catalogue
```bash
curl --location 'http://127.0.0.1:8000/api/catalogue/list' \
--header 'Authorization: Bearer <access_token>'
```
