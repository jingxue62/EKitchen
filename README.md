Project EKitchen

Install

Requirements:
- python3
- pip
- venv
- django


python3 -m venv EK-venv 
source EK-venv/bin/activate
pip install Django



Exit venv:

deactivate


Initialization:
django-admin startproject EKitchen .


Run Server:
python manage.py runserver

Migration:
python manage.py migrate

Create tables:
python manage.py makemigrations EKitchen
(Recommand to preview the SQL first, 'sqlmigrate')
python manage.py migrate

View SQL queries:
python manage.py sqlmigrate EKitchen 0001

Shell:
python manage.py shell

DBShell:
python manage.py dbshell

>.tables
> select * from <table name>;

Prepopulate data:
python manage.py loaddata ./EKitchen/fixtures.json 


Ref:
https://docs.djangoproject.com/en/4.1/intro/tutorial01/
https://docs.djangoproject.com/en/4.1/intro/tutorial02/
https://docs.djangoproject.com/en/4.1/topics/db/queries/