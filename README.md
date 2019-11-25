## Development and testing environments

  - Docker Compose (1.24.1, build 4667896b)
  - Docker  (1.13.1, build 092cba3)
  - Python docker image (python:3.7-alpine)
  - PostgreSQL docker image (postgres:11-alpine)
  - Redis docker image (redis:alpine)


## How to run the application

Make sure that docker-compose and docker are installed on your system. Clone the repository and then change directory to the cloned repository.

Build the application

```sh
docker-compose build
```

Run the database migrations

```sh
docker-compose up init
```

Run the web application, celery worker, celery beat and the monitor

```sh
docker-compose up -d web celery-worker celery-beat monitor
```

## Application URL

- [http://localhost:8000/](http://localhost:8000/)

## How to run tests

Run the tests

```sh
docker-compose up test
```
