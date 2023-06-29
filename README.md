# ElevatorSystemSolution

The elevator system with N number of elevator is to decide whether the elevator should go up, go down, or stop. We'll ignore a lot of what goes into a real world elevator, like physics, maintenance overrides, and optimizations for traffic patterns. Now some user comes in and makes a request to an elevator. The elevator automatically moves UP/DOWN as per the request of the user. The status of an elevator like it is currently operational or not can be updated using API calls.

## Installation : 
1. Make a python virtual enviornment in your preferred Linux/WSL2...any system
```
Recommended python version -----> 3.7.X (The LATEST STABLE RELEASE)
```

2. Clone the repo and navigate to the directory where the manage.py file is located
```
git clone https://github.com/akarshkumarmadhwa/ElevatorSystemSolution.git
```
```
cd ElevatorSystemSolution/elevator_system
```

3. Please make sure you enter the correct directoryy containing the project.

4. Install the requirements
```
pip install -r requirements.txt
```
5. Next, update the elevator_system/settings.py file to configure the database as suggested to use PostgreSQL:
```
Postgres Database Installation:-
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
RELEASE=$(lsb_release -cs)
echo "deb http://apt.postgresql.org/pub/repos/apt/ ${RELEASE}"-pgdg main | sudo tee  /etc/apt/sources.list.d/pgdg.list
sudo apt update
sudo apt install postgresql-11
------------------------------or----------------------------
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo apt install postgresql postgresql-contrib
Connect to postgres with command sudo -u postgres psql

 CREATE USER user WITH PASSWORD 'password';
 CREATE DATABASE "elevator_system_db" WITH OWNER "user" ENCODING 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8' TEMPLATE template0;
 ALTER ROLE user SET client_encoding TO 'utf8';
 ALTER ROLE user SET default_transaction_isolation TO 'read committed';
 ALTER ROLE user SET timezone TO 'UTC';
 GRANT ALL PRIVILEGES ON DATABASE elevator_system_db TO user;
 \q

# Configure the database (PostgreSQL example)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'elevator_system_db',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

```
6. Run the development server
```
python manage.py runserver
```
