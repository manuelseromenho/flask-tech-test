# Flask Tech Test

## Getting Started

This project uses python3. A pip requirements.txt file is included to install the dependencies (SQLAlchemy, Dictalchemy, Flask)

## Running with Docker
- A sample Dockerfile and docker-compose.yml are provided that will run the application in an isolated environment

- Make sure you have `docker` installed and that the Docker daemon is running
- Make sure you have `docker-compose` installed and running

- Build the image/run container with docker-compose: `docker-compose up`

- Start making some requests: `curl http://localhost:5000/articles`

## Project Structure Notes

- The database models are stored in the `techtest/models` folder
- The routes of the Flask app are in `techtest/routes` folder

In both cases, the modules are loaded by using the `__all__` variable in `__init__.py`, so be sure to update this if you add new files.

## Tasks

- Add an new entity called `Author` with a `first_name` and a `last_name`. An API user should be able to create a new `Author`, edit an existing one and list all existing ones.
- Update the `Article` entity so that it relates to an `Author`. An API user should now be able to select an `Author` when creating or editing an `Article`.
- write unit tests to check that the new routes you created for `Author` are automically tested.
