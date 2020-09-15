# service-name

| Branch | Status |
|--------|-----------|
| develop | ![Build Status](<codebuild-badge>) |
| master | ![Build Status](<codebuild-badge>) |

## Summary of the project

A simple description of the service should go here

## How to run locally

### dependencies

The **Make** targets assume you have **bash**, **curl**, **tar**, **docker** and **docker-compose** installed.

### Setting up to work

First, you'll need to clone the repo

    git clone git@github.com:geoadmin/service-name

Then, you can run the dev target to ensure you have everything needed to develop, test and serve locally

    make dev

That's it, you're ready to work.

### Linting and formatting your work

In order to have a consistent code style the code should be formatted using `yapf`. Also to avoid syntax errors and non
pythonic idioms code, the project uses the `pylint` linter. Both formatting and linter can be manually run using the
following command:

    make format-lint

**Formatting and linting should be at best integrated inside the IDE, for this look at
[Integrate yapf and pylint into IDE](https://github.com/geoadmin/doc-guidelines/blob/master/PYTHON.md#yapf-and-pylint-ide-integration)**

### Test your work

Testing if what you developed work is made simple. You have four targets at your disposal. **test, serve, gunicornserve, dockerrun**

    make test

This command run the integration and unit tests.

    make serve

This will serve the application through Flask without any wsgi in front.

    make gunicornserve

This will serve the application with the Gunicorn layer in front of the application

    make dockerrun

This will serve the application with the wsgi server, inside a container.
To stop serving through containers,

    make shutdown

Is the command you're looking for.

## Endpoints

all trailing slashes are optionals

### /checker/ [GET]

#### description of the route

this is a simple route meant to test if the server is up.

#### parameters

None

#### expected results

##### Success

    "OK", 200

## Deploying the project and continuous integration

When creating a PR, terraform should run a codebuild job to test, build and push automatically your PR as a tagged container.

This service is to be delployed to the Kubernetes cluster once it is merged.

TO DO: give instructions to deploy to kubernetes.

### Deployment configuration

The service is configured by Environment Variable:

| Env         | Default               | Description                            |
|-------------|-----------------------|----------------------------------------|
| LOGGING_CFG | logging-cfg-local.yml | Logging configuration file             |
