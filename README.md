# ProjectPod-API
This is a project management application where users can join a workspace and them will ba able to create projects, teams, and tasks. These all work together to ensure smooth management of projects which inturn improves effieciency and productivity.
This robust API can be utilized with any platform, be it web or mobile platforms.

## Features
* Users can create account, verify their email, choose a subscription plan, login, update their details, log out, delete their account 
* Users can create and be added a workspace by the author or editor in the workspace. The number of workspaces a user can be a part of is limited to the user's subscription plan.
* Users that have the access can create projects in the workspace. The number of projects is limited based on the subscription plan for the workspace.
* Users that have the access can create teams in the workspace.
* Users that have the access can create tasks in the workspace. Tasks can either be team based or project based.
* Users can comment on projects and the comments can be replied to as well.
* Users can send notifications to other users.

## Documentation
The postman documentation can be found (here)[https://documenter.getpostman.com/view/25448393/2sA3Bj9EAx#f8a7683b-b159-4a24-ad98-98263e9f38cf]

## Set up on local machine
1. Clone the project by using the command in the terminal: `git clone https://github.com/joboy-dev/Project-Management-API.git`
2. Run the following commands:
    #### Windows
    * *`pip install -r requirements.txt` to get the necessary dependencies
    * *`py manage.py makemigrations` to have a database file
    * *`py manage.py migrate`
    * *`py manage.py collectstatic` which is essential for the ckeditor5 used in the project for creating and editing a project.
    * *`py manage.py runserver` to start up the develeopment server

    #### macOS/Linux
    * *`pip install -r requirements.txt` to get the necessary dependencies
    * *`python3 manage.py makemigrations` to have a database file
    * *`python3 manage.py migrate`
    * *`python3 manage.py collectstatic` which is essential for the ckeditor5 used in the project for creating and editing a project.
    * *`python3 manage.py runserver` to start up the develeopment server
3. Create a `.env` file in the root directory of the project and add a `SECRET_KEY` variable:
    `SECRET_KEY = 'random characters'`
4. Create a `media` folder in the root directory of the project as well.

### OPTIONAL
You can create a virtual environment before running the commands in number 2.

#### Creating the Virtual Environment
* *Open your terminal or command prompt.
* *Navigate to the directory where you want to create your virtual environment.
* *Execute the following command:
    `python -m venv /path/to/new/virtual/environment`
* *Replace /path/to/new/virtual/environment with the desired location for your virtual environment. For example:
    `python -m venv .venv`
* *This will create a virtual environment in the current directory.
* *On Windows, you can also use the following command:
    `python -m venv c:\path\to\myenv`

Just do `python-m venv venv` to put the virtual environment in the project root directory

#### Activate the Virtual Environment
After creating the virtual environment, activate it:
* *On Windows:
    `.venv\Scripts\activate`

* *On macOS/Linux:
    `source .venv/bin/activate`

#### Deactivate the Virtual Environment
When you’re done working in the virtual environment, deactivate it:
    `deactivate`