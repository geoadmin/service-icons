# service-icons

| Branch  | Status                                                                                                                                                                                                                                                                                                                      |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| develop | ![Build Status](https://codebuild.eu-central-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoianNmckV3aUxNR01rMDBCNWpwQlBjY3lvRDh0d1pXeExJc0EzTG82d0IxbUJYNEVjaDdiR3VsY1VqS1dXVlFQOHBsZW81cVo3WTkvOHVnd1dreC9sWDZFPSIsIml2UGFyYW1ldGVyU3BlYyI6IkNLS1hoTFB1bitMQkYxNTEiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=develop) |
| master  | ![Build Status](https://codebuild.eu-central-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoianNmckV3aUxNR01rMDBCNWpwQlBjY3lvRDh0d1pXeExJc0EzTG82d0IxbUJYNEVjaDdiR3VsY1VqS1dXVlFQOHBsZW81cVo3WTkvOHVnd1dreC9sWDZFPSIsIml2UGFyYW1ldGVyU3BlYyI6IkNLS1hoTFB1bitMQkYxNTEiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)  |

## Table of content

- [Table of content](#table-of-content)
- [Description](#description)
- [Dependencies](#dependencies)
- [Service API](#service-api)
- [Versioning](#versioning)
- [Local Development](#local-development)
  - [Make Dependencies](#make-dependencies)
  - [Setting up to work](#setting-up-to-work)
  - [Linting and formatting your work](#linting-and-formatting-your-work)
  - [Test your work](#test-your-work)
- [Docker](#docker)
- [Maintenance](#maintenance)
  - [Convert Symbols from svg to png](#convert-symbols-from-svg-to-png)
- [Deployment](#deployment)
  - [Deployment configuration](#deployment-configuration)

## Description

A simple REST microservice meant to take a symbol (defined by a filename), to colorized it with a color defined by r, g and b values and to return the colorized symbol.

## Dependencies

This service doesn't have any external dependencies

## Service API

The service has the following endpoints:

- `GET /checker`
- `GET /sets`
- `GET /sets/<icon_set_name>`
- `GET /sets/<icon_set_name>/icons`
- `GET /sets/<icon_set_name>/icons/<icon_name>`
- `GET /sets/<icon_set_name>/icons/<icon_name>.png`
- `GET /sets/<icon_set_name>/icons/<icon_name>-<red>,<green>,<blue>.png`
- `GET /sets/<icon_set_name>/icons/<icon_name>@<scale>.png`
- `GET /sets/<icon_set_name>/icons/<icon_name>@<scale>-<red>,<green>,<blue>.png`

A detailed descriptions of the endpoints can be found in the [OpenAPI Spec](https://github.com/geoadmin/doc-api-specs) repository.

## Versioning

This service uses [SemVer](https://semver.org/) as versioning scheme. The versioning is automatically handled by `.github/workflows/main.yml` file.

See also [Git Flow - Versioning](https://github.com/geoadmin/doc-guidelines/blob/master/GIT_FLOW.md#versioning) for more information on the versioning guidelines.

## Local Development

### Make Dependencies

The **Make** targets assume you have **python3.9**, **pipenv**, **bash**, **curl**, **tar**, **docker** and **docker-compose** installed.

### Setting up to work

First, you'll need to clone the repo

```bash
git clone git@github.com:geoadmin/service-icons
```

Then, you can run the setup target to ensure you have everything needed to develop, test and serve locally

```bash
make dev
```

That's it, you're ready to work.

### Linting and formatting your work

In order to have a consistent code style the code should be formatted using `yapf`. Also to avoid syntax errors and non
pythonic idioms code, the project uses the `pylint` linter. Both formatting and linter can be manually run using the
following command:

```bash
make format-lint
```

**Formatting and linting should be at best integrated inside the IDE, for this look at
[Integrate yapf and pylint into IDE](https://github.com/geoadmin/doc-guidelines/blob/master/PYTHON.md#yapf-and-pylint-ide-integration)**

### Test your work

Testing if what you developed work is made simple. You have four targets at your disposal. **test, serve, gunicornserve, dockerrun**

```bash
make test
```

This command run the integration and unit tests.

```bash
make serve
```

This will serve the application through Flask without any wsgi in front.

```bash
make gunicornserve
```

This will serve the application with the Gunicorn layer in front of the application

```bash
make dockerrun
```

This will serve the application with the wsgi server, inside a container.

Here below are simple examples of how to test the service after serving on localhost:5000:

```bash
curl -H "Origin: www.example.com" http://localhost:5000/sets/default/icons
curl -H "Origin: www.example.com" http://localhost:5000/sets/default/icons/001-marker@2x-255,133,133.png --output out.png
```

*NOTE: if you serve using gunicorn or docker, you need to add the route prefix `/api/icons`*

## Docker

The service is encapsulated in a Docker image. Images are pushed on the `swisstopo-bgdi-builder` account of [AWS ECR](https://eu-central-1.console.aws.amazon.com/ecr/repositories?region=eu-central-1) registry. From each github PR that is merged into develop branch, one Docker image is built and pushed with the following tags:

- `develop.latest`
- `CURRENT_VERSION-beta.INCREMENTAL_NUMBER`

From each github PR that is merged into master, one Docker image is built and pushed with the following tag:

- `VERSION`

Each image contains the following metadata:

- author
- git.branch
- git.hash
- git.dirty
- version

These metadata can be seen directly on the dockerhub registry in the image layers or can be read with the following command

```bash
# NOTE: jq is only used for pretty printing the json output,
# you can install it with `apt install jq` or simply enter the command without it
docker image inspect --format='{{json .Config.Labels}}' 974517877189.dkr.ecr.eu-central-1.amazonaws.com/service-name:develop.latest | jq
```

You can also check these metadata on a running container as follows

```bash
docker ps --format="table {{.ID}}\t{{.Image}}\t{{.Labels}}"
```

## Maintenance

### Convert Symbols from svg to png

Sometimes it may happen, that we get a new set of icons. In general these icons have to be quadratic in a resolution of 48px x 48px in the format .png. Neverthanless there is a script to convert .svg images towards .png images. This script is located in the folder `scripts/svg2png.py`. There is a help provided

```bash
pipenv run python scripts/svg2png.py --help
```

Here is an example of such a convertion

```bash
pipenv run python scripts/svg2png.py --help
```pipenv run python scripts/svg2png.py -I ./tmp/new-icons -O ./static/images/babs2 -W 48 -H 48
```

## Deployment

### Deployment configuration

The service is configured by Environment Variable:

| Env         | Default               | Description                |
| ----------- | --------------------- | -------------------------- |
| LOGGING_CFG | `logging-cfg-local.yml` | Logging configuration file |
| ALLOWED_DOMAINS | `.*` | Comma separated list of regex that are allowed as domain in Origin header |
| CACHE_CONTROL | `public, max-age=86400` | Cache Control header value of the `GET /*` endpoints |
| CACHE_CONTROL_4XX | `public, max-age=3600` | Cache Control header for 4XX responses |
| FORWARED_ALLOW_IPS | `*` | Sets the gunicorn `forwarded_allow_ips`. See [Gunicorn Doc](https://docs.gunicorn.org/en/stable/settings.html#forwarded-allow-ips). This setting is required in order to `secure_scheme_headers` to work. |
| FORWARDED_PROTO_HEADER_NAME | `X-Forwarded-Proto` | Sets gunicorn `secure_scheme_headers` parameter to `{${FORWARDED_PROTO_HEADER_NAME}: 'https'}`. This settings is required in order to generate correct URLs in the service responses. See [Gunicorn Doc](https://docs.gunicorn.org/en/stable/settings.html#secure-scheme-headers). |
| SCRIPT_NAME | `''` | If the service is behind a reverse proxy and not served at the root, the route prefix must be set in `SCRIPT_NAME`. |
| WSGI_TIMEOUT | `5` | WSGI timeout. |
| GUNICORN_TMPFS_DIR | `None` |The working directory for the gunicorn workers. |
| WSGI_WORKERS | `2` | The number of workers per CPU. | 
