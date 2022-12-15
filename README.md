# URL Shortener with FastAPI
Sample API to shorten long urls to short links
## How to run 

```shell
$ cd urlShortener
$ docker-compose build
$ docker-compose up
$ docker-compose exec api alembic upgrade head # to run first time to create database tables 
```


## How to test

```shell
$ docker-compose -f docker-compose.test.yml build 
$ docker-compose -f docker-compose.test.yml run --rm test alembic upgrade head # to run first time to create test database tables
$ docker-compose -f docker-compose.test.yml run --rm test pytest -v # run tests
```