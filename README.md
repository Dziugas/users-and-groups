# User management app
Create Users and assign them to Groups.

## Using Docker for dev environment
Build the project:

`docker-compose build`

Run the project:

`docker-compose up`

### Running migrations, tests and linter with Docker
Enter the web app's Docker container:

`docker exec -it management bash`

Run database migrations:

`python manage.py migrate`

Run tests:

`coverage run manage.py test`

Run linter:

`flake8`

There is an option to use the Black formatter for code styling.

## Authentication and Authorization

To get the auth token send a POST request with user credentials to 
the following endpoint:

`api-token-auth/`

Example data for such POST request:
```
{
    "username": "admin",
    "password": "xxxxxxxx"
}
```

A superuser can be created inside web app's Docker container 
with the following command: `python manage.py createsuperuser`


All further endpoints require Token Authentication, therefore make sure to 
include the following header in each request:

`Authorization:Token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`


## Other Endpoints

* ### Users

    `/api/users/`

    Accepts `GET` and `POST` requests.

    Retrieves a list of existing users or allows to create new 
user instances. 

    Example data for creating a new user:
    ```
    {
        "username": "JD",
        "first_name": "John",
        "last_name": "Doe",
        "email": "jd@example.com"
    }
    ```
    `api/users/{id}/`

    Accepts `GET, PUT, PATCH, DELETE` requests.

    Retrieve, update or delete specific user instances.

* ### Groups

    `/api/groups/`

    Accepts `GET` and `POST` requests.

    Retrieves a list of existing groups or allows to create new 
    groups.

    To create a group only a name is required, e.g.:
    ```
    {
        "name" : "Gamers"
    }
    ```
    `api/groups/{id}/`

    Accepts `GET, PUT, PATCH, DELETE` requests.

    Retrieve, update or delete specific group instances.

    `api/groups/{id}/add-user/`

    Accepts `POST` requests.

    Add user to a group. For this user id is required, e.g.:
    ```
    {
        "id" : 1
    }
    ```

    `api/groups/{id}/remove-user/`

    Accepts `DELETE` requests.

    Remove user from a group. For this user id is required, e.g.:
    ```
    {
        "id" : 1
    }
    ```