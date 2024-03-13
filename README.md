## FastAPI Social Media API
Backend clone of a social media app built with FastAPI.

## API Routes
The API contains 4 main routes:
1. Post Route
    -  Responsible for creating, deleting, updating posts and checking posts
2. Users Route
    - Handles creating and searching users by ID
3. Auth Route
    - Manages user authentication and login
4. Vote Route
    - Supports likes/votes, includes code for upvoting and backing votes

## Getting Started
To run the API locally:

1. Clone the repo:
```
git clone https://github.com/SergeyRogonov/example-fastapi.git
```
2. Change to project directory:
```
cd fastapi-course
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Run the dev server:
```
uvicorn main:app --reload
```
5. Browse the API docs: 
```
http://127.0.0.1:8000/docs
```

## To run this API you need a Postgresql database and set the environment variables for it
Create a database in postgres then create a file name ```.env``` and write the following things in you file
```
DATABASE_HOSTNAME = db_hostname(localhost)
DATABASE_PORT = db_port(5432)
DATABASE_PASSWORD = db_password
DATABASE_NAME = db_name
DATABASE_USERNAME = db_user_name
SECRET_KEY = 09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7(to get a string like this run: openssl rand -hex 32)
ALGORITHM = algorithm(e.g. HS256)
ACCESS_TOKEN_EXPIRE_MINUTES = 60(base)
```
