# Project EKitchen

## Install

### Requirements:
- python3
- pip
- venv
- django


### Enter Virtual env
python3 -m venv EK-venv 
source EK-venv/bin/activate
pip install Django

### To solve the sqlite3 version issue on AL2
see: https://stackoverflow.com/questions/57214850/trying-to-upgrade-sqlite-on-amazon-ec2

### Exit venv:

deactivate


### Initialization:
django-admin startproject EKitchen .


## Run Server:
python manage.py runserver

### Migration:
python manage.py migrate

### Create tables:
python manage.py makemigrations EKitchen
(Recommand to preview the SQL first, 'sqlmigrate')
python manage.py migrate

### View SQL queries:
python manage.py sqlmigrate EKitchen 0001

### Shell:
python manage.py shell

### DBShell:
python manage.py dbshell

```
>.tables
> select * from <table name>;
```

### Prepopulate data:
python manage.py loaddata ./EKitchen/fixtures.json 


## Cache service
We use redis for the caching.

### Redis install:
https://redis.io/download/
Or:
```brew install redis```

### Run Redis server
```$ redis-server```

### Test
```$ redis-cli ping```

See the output: "PONG"

### Install django-redis
```python -m pip install django-redis```

### Django settings
In `settings.py`:
```CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "ek"
    }
}
```

## Remote database setup
On AL2: `sudo amazon-linux-extras install postgresql12`
http://howto.philippkeller.com/2022/05/03/How-to-install-postgres-on-amazon-linux-2/

`pip install psycopg2-binary` on Django side to use postgresql


# Ref:
https://docs.djangoproject.com/en/4.1/intro/tutorial01/
https://docs.djangoproject.com/en/4.1/intro/tutorial02/
https://docs.djangoproject.com/en/4.1/topics/db/queries/
