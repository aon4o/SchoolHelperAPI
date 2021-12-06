# SchoolHelperAPI

## Project Installation

### **Important!**

* **To install this project you need `Python3` and `pip`!**
* **To be able to set up the database you will need `PostgreSQL`!**

### FastAPI Setup

* Installing the dependencies - `pip install -r requirements.txt`
* Environmental variables - you should create a `.env` file in the root directory of the project using the template `.env.example` and fill in the corresponding information

### DataBase Setup

To login as an administrator use the command `sudo -iu postgres`, then `psql`.

Default DataBase Setup:

* CREATE DATABASE school_helper;
* CREATE USER school_helper WITH ENCRYPTED PASSWORD 'school_helper';
* ALTER ROLE school_helper SET client_encoding TO 'utf8';
* ALTER ROLE school_helper SET default_transaction_isolation TO 'read committed';
* ALTER ROLE school_helper SET timezone TO 'UTC';
* GRANT ALL PRIVILEGES ON DATABASE school_helper TO school_helper;

For dumping and restoring the information in the database use:

- `pg_dump -h localhost -U school_helper -d school_helper -f school_helper.sql` for dumping the database
- `psql -h localhost -U school_helper -d school_helper -f school_helper.sql` for restoring the database

## Running the Server

`uvicorn main:app --reload`
