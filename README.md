# service-color

| Branch | Status |
|--------|-----------|
| develop | ![Build Status](https://codebuild.eu-central-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoicXJCdkRTRUhuY28yU0N5ZXJVM1hjSnc0Tk5ZWjV3Z25RYWNWOURTeWx2QkpOYXFQRk8wMkZ3a3BJMVZJU2h5bTcyMGtkY29UYWxiNENNVERhUUl2Tjh3PSIsIml2UGFyYW1ldGVyU3BlYyI6InF0ZXJIb0doTERqcndTamoiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=develop) |
| master | ![Build Status](https://codebuild.eu-central-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoicXJCdkRTRUhuY28yU0N5ZXJVM1hjSnc0Tk5ZWjV3Z25RYWNWOURTeWx2QkpOYXFQRk8wMkZ3a3BJMVZJU2h5bTcyMGtkY29UYWxiNENNVERhUUl2Tjh3PSIsIml2UGFyYW1ldGVyU3BlYyI6InF0ZXJIb0doTERqcndTamoiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master) |

## Table of content

- [Description](#description)
- [Dependencies](#dependencies)
- [Service API](#service-api)
- [Local Development](#local-development)
- [Deployment](#deployment)


## Description

A simple REST microservice meant to take a symbol (defined by a filename), to colorized it with a color defined by r, g and b values and to return the colorized symbol.

## Dependencies

This service doesn't have any external dependencies

## Service API

This service has two endpoints:

- [checker GET](#checker-get)
- [color GET](#color-get)

A detailed descriptions of the endpoints can be found in the [OpenAPI Spec](openapi.yaml).


### Staging Environments

| Environments | URL |
|--------------|-----|
| DEV          | [https://service-color.bgdi-dev.swisstopo.cloud/v4/color/](https://service-color.bgdi-dev.swisstopo.cloud/v4/color/)  |
| INT          | [https://service-color.bgdi-int.swisstopo.cloud/v4/color/](https://service-color.bgdi-int.swisstopo.cloud/v4/color/)  |
| PROD         | [https://service-color.bgdi-prod.swisstopo.cloud/v4/color/](https://service-color.bgdi-int.swisstopo.cloud/v4/color/) |


### checker GET

This is a simple route meant to test if the server is up.

| Path | Method | Argument | Response Type |
|------|--------|----------|---------------|
| /v4/color/checker | GET | - | application/json |

### color GET

This route takes a color (defined by r, g and b values) and the name of a file containing a symbol to be colorized
and returns the colorized symbol.

| Path | Method | Argument | Response Type |
|------|--------|----------|---------------|
| /v4/color | GET | r, g, b, filename | image/png |


## Local Development

### Make Dependencies

The **Make** targets assume you have **bash**, **curl**, **tar**, **docker** and **docker-compose** installed.

### Setting up to work

First, you'll need to clone the repo

    git clone git@github.com:geoadmin/service-color

Then, you can run the setup target to ensure you have everything needed to develop, test and serve locally

    make setup

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

    curl -H "Origin: https://map.geo.admin.ch/" http://localhost:5000/v4/color/255,133,133/marker-24@2x.png --output out.dat

This is a simple example of how to test the service after serving on localhost:5000 (`out.dat` will either contain a PNG image or contain an error message.)


## Deployment

This service is to be deployed to the Kubernetes cluster once it is merged.

TO DO: give instructions to deploy to kubernetes.

### Deployment configuration

The service is configured by Environment Variable:

| Env         | Default               | Description                            |
|-------------|-----------------------|----------------------------------------|
| LOGGING_CFG | logging-cfg-local.yml | Logging configuration file             |
