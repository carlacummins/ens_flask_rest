# Sample REST API

This repo contains a basic REST API for fetching genes from Ensembl. It is based on Python and Flask. 

## Setup

From inside your vagrant VM (as detailed [here](https://github.com/joanmarcriera/vagrant-file)), you will need to follow these steps:
```
$ git clone https://github.com/carlacummins/ens_flask_rest.git
$ cd ens_flask_rest

$ docker build -t ens_flask_rest .
$ docker run -p 80:5000 --name py_rest_ens ens_flask_rest
```
Port 5000 is exposed and mapped to vagrant's port 80. By default, vagrant's port 80 is mapped to `localhost:8080`, but see your `Vagrantfile` for details.

## Endpoint(s)

This API only has a single endpoint: `/gene/`. Full [Swagger](https://swagger.io/) documentation is available at `localhost:8080/api/docs`

## Unit Tests

A small test suite has been included with this application. It is implemented with [unittest2](https://pypi.org/project/unittest2/). Docker automatically runs these upon building, but if you wish to run the tests manually, you can use the following commands (after `docker run`):
```
# open a shell inside the docker container
$ docker exec -it py_rest_ens bash
# run the tests
$ unit2 discover -v -s /usr/src/
```
