## PyHospital Setup

- `git clone https://github.com/girishmahale786/pyhospital.git`

- Create Virtual Environment `virtualenv venv`

- Activate Virtual Environment
    - Windows - `venv/Scripts/activate.ps1`
    - Linux - `source venv/bin/activate`

- Install Dependencies `pip install -r requirements.txt`

- Make Migratations `python manage.py makemigrations`

- Run Migratations `python manage.py migrate`

- Create Super User `python manage.py createsuperuser`
    - Enter Username and Password and Create Super User

- Start Server `python manage.py runserver`
