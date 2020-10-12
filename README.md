---
title: 'SDA-metadata-submission-api'
---

Requirements
============

-   Python 3.7.0
-   MongoDB 4.0.4 
-   Docker \>= 17.10
-   (optional) docker-compose \>= 1.16.1

Development Setup
=================

There are two ways to set-up the project in local development environment:
1. Using docker-compose (recommended)
2. Set up the project in a virtualenv and run the servers locally.

 In general, the following steps can be your guide for setting a local
development environment:

``` {.sourceCode .bash}
# Clone the repository and cd into it
$ git clone {git@git.computerome.dk:data-visualisation/cge-query-api.git}
$ cd SDA-metadata-submission-api

# Create your virtualenv, using pyenv for example (highly recommended: https://github.com/pyenv/pyenv)
$ pyenv virtualenv 3.7.0 cge-query-api-dev

# From within the root directory and with an active virtualenv, install the dependencies and package itself
$ pip install -e .
```

Running a Development Instance
------------------------------

# Running server locally with development configuration
``` {.sourceCode .bash}

With the virtual enviorment created we activate it running:
$ pyenv activate cge-query-api-dev
Set FLASK environment variable to development, so changes in the code are inmediatelly used:
$ export FLASK_ENV=development
Then proceed to run the flask server by running the command:
$ flask run
```

# Running server locally with docker compose
Make sure that you have the images downloaded from gitlab server. If not build the images in cge-api and cge-pipeline folder using the command 

``` {.sourceCode .bash}
# Build cge-api image inside cge-api folder
$ docker build -t cge-api .

# Build cge-api image inside cge-pipeline folder
$ docker build -t cge-pipeline .
```

``` {.sourceCode .bash}
# Bring the service up in a container.
$ docker-compose up --build
```
