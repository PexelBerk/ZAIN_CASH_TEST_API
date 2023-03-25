# ZAIN CASH TEST API

zain cash test API that is created as a clone for test.zaincash.iq  

Zain cash test API is very limited and I can't really have any account that have enough money to give me
success message so I decided to create this clone to test with it.  

See documentation about the zain cash API here:  
https://docs.zaincash.iq/





# Setting Up the Project locally

## Prerequisites
Before starting, you should have the following installed on your system:
- Python (version 3.10.8 or above)
- pip (Python package installer)

## Creating a Virtual Environment
1. Create a new directory for your project.
2. Open a terminal or command prompt and navigate to the new directory.
3. Create a new virtual environment by running the following command:
    ```
    python -m venv env
    ```
    This will create a new folder called `env` in your project directory, which will contain all the necessary packages for your project.
4. Activate the virtual environment by running the following command:
    - On Windows: 
    ```
    env\Scripts\activate
    ```
    - On Linux or macOS:
    ```
    source env/bin/activate
    ```

## Installing Django and Other Packages
1. With the virtual environment activated, run the following command to install all the necessary packages & libraries for python:
    ```
    pip install -r requirements.txt
    ```

## Creating a .env File

The `.env` file contains all the sensitive information about the project 

1. Create a new file in your project directory called `.env`.
2. Add your sensitive information as environment variables in the following format:
    ```
    SECRET_KEY=this is my SECRET_KEY
    DEBUG=1
    ```

    **hint:**
    The information are all development information and credentials. 


    **Django credentials:**
    - SECRET_KEY: django secret key.
    - DEBUG: set to `1` as `True` in development enviroment.    




## Migrations  

Migrate the database changes using this command in the directory of the project 
```
python manage.py migrate
```

and this will create a new file called `db.sqlite3` that is the database for development enviroment.


## Running the project  

Run the project using this command in the directory of the project.

~~~
python manage.py runserver 8001
~~~

**hint:** running on port `8001` to avoid conflicts with other projects  

# Using the Project

## Create super user

open the terminal in the project directory and run this command

```
python manage.py createsuperuser
```

fill the username, email, password and confirm password   

## Access Admin Panel

After running the project go this url `http://127.0.0.1:8001/admin`.   
Enter the username and password of the superuser that you have created  
You will see few DataBase tables in Base section:  

1. Accounts: the users accounts (as they are zain cash wallet)
2. Merchants: the merchants 
3. Transaction: the transactions

you can easly add new Accounts, Merchants  

the Transaction will be created by using the API by following the zain cash documentation. 






