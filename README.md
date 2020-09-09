# Mapt

Shape file sharing application, testing out RMWC as a component framework

# Dev Environment

The development environment is containerised using the `docker-compose.yml` file. This file mounts both the frontend
and backend source code directories. This means hot reloading still works in the containerised environment.

## Setup

The setup requires node, pre-commit and docker-compose as dependencies. I am using node v14.8.0
In order to setup the development environment you should run:

```
make setup
```

This will run `yarn-install` for the front-end libraries, this isn't in the container but in my experience it helps
with my IDE (pyCharm) with code completion. It will then also run yarn-install in the root directory to install the
openapi code generator to help keep the front-end client in sync with the backend as you update it. It will then
build the Docker images for both the frontend and backend.

## Environment Variables

The setup process will have also created two `.env` files in the frontend and backend directories. Currently the
required entries in `frontend/.env` are:

```
REACT_APP_MAPBOX_ACCESS_TOKEN=
```

And in the backend they are:

```
# None yet!
```

## Running the Application

To run the application simply run:

```
make run-stack
```

Once you have supplied the required environment variables

## Add a Backend Dependency

As the development environment is containerised the Docker image needs to rebuilt after running
pip install in the container. To add a new (or multiple) dependency use the command:

```
make pip-install <MY_PACKAGE> <MY_PACKAGE_2>
```

This command will execute pip-install in the container and then refresh the requirements.txt which is mounted in the
`docker-compose.yml` file

# Add a Frontend Dependency

To do this run:

```
make yarn-add <MY_PACKAGE>
```

Again this will run in the container but will also run `yarn install` locally because otherwise your local
`node_modules` will be out of sync with the containers

# Updating the Frontend OpenAPI client

This application make use of the fact that FastAPI generates an OpenAPI spec for you when you define the API. To
refresh the `frontend/src/client` package first up the stack and then type:

```
make regen-openapi-client
```

ESLint should be able to pretty easily pick up if there has been a breaking change (such as field removal)

# Linting

To run all the linters this project uses pre-commit. To run the linters run:

```
make lint
```
