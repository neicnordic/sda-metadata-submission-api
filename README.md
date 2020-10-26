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
$ git clone {https://github.com/neicnordic/sda-metadata-submission-api.git}
$ cd SDA-metadata-submission-api

# Create your virtualenv, using pyenv for example (highly recommended: https://github.com/pyenv/pyenv)
$ pyenv virtualenv 3.7.0 metadata-api-dev


```

Running a Local Instance
------------------------------
``` {.sourceCode .bash}

- cd into app;
- activate the new virtualenv created by typing 'pyenv activate <env_name>';
- enter flask run
```

Running a Local Test
------------------------------
``` {.sourceCode .bash}

In order to run a local test you either call the 'tox' command from the directory root
or:

- cd into app/tests;
- enter pytest -vvv test_api.py;

```

# Running server locally with docker compose

``` {.sourceCode .bash}
# Bring the service up in a container.
$ docker-compose up --build
```
