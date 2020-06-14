# Fridgify's Backend

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/4789c22f04534c10aaca950aa3393bfc)](https://www.codacy.com/gh/Fridgify/Fridgify_Backend?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Fridgify/Fridgify_Backend&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/4789c22f04534c10aaca950aa3393bfc)](https://www.codacy.com/gh/Fridgify/Fridgify_Backend?utm_source=github.com&utm_medium=referral&utm_content=Fridgify/Fridgify_Backend&utm_campaign=Badge_Coverage)
![Docker hub builds](https://img.shields.io/docker/cloud/build/fridgify/fridgify)
![Docker hub automated builds](https://img.shields.io/docker/cloud/automated/fridgify/fridgify)

| | | | |
| - | - | - | - |
| Production | ![Docker image size production server](https://img.shields.io/docker/image-size/fridgify/fridgify/latest) | ![Docker version production server](https://img.shields.io/docker/v/fridgify/fridgify/latest?color=blue) | ![Teamcity build production](https://img.shields.io/teamcity/build/e/Fridgify_DeployFridgifyProduction?server=https%3A%2F%2Ffridgify-tc.donkz.dev) | [![Teamcity build production](https://img.shields.io/website?label=documentation&url=https%3A%2F%2Ffridgapi-dev.donkz.dev%2F)](https://fridgapi.donkz.dev/)
| Development | ![Docker image size develop server](https://img.shields.io/docker/image-size/fridgify/fridgify/develop-latest) | ![Docker version develop server](https://img.shields.io/docker/v/fridgify/fridgify/develop-latest?color=blue) | ![Teamcity build production](https://img.shields.io/teamcity/build/e/Fridgify_DeployFridgifyDevelopment?server=https%3A%2F%2Ffridgify-tc.donkz.dev) | [![Teamcity build development](https://img.shields.io/website?label=documentation&url=https%3A%2F%2Ffridgapi-dev.donkz.dev%2F)](https://fridgapi-dev.donkz.dev/)


***Stay cool. Stay organized.*** <br/>
Fridgify is an application focused on managing fridges quickly and easily. <br/>
* barcode scan products
* manage multiple fridges
* invite friends & family

## Features
* centralized product database (add items manually/via barcode)
* add multiple fridges
* invite other users via link or barcode
* manage roles for certain fridges
* synced on multiple devices
* available on Play Store
* communicate via REST API

## Setup
### Requirements
Before setting up Fridgify's backend, make sure you have the following tools set up:
* [Docker](https://docs.docker.com/engine/install/)
* [docker-compose](https://docs.docker.com/compose/install/)
* [Firebase](https://firebase.google.com/)*
  * [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging)
  * [Firebase Dynamic Links](https://firebase.google.com/docs/dynamic-links)

\* Firebase is required for Fridgify's messaging service as well as invitations. So make sure to create a project in Firebase and set up Cloud Messaging and Dynamic Links.

Be sure to also prepare an environment file, based on the environment variables given [here](#environment).

## Installation
There are two ways to deploy Fridgify's backend:

· [Install via Docker image](#install-via-docker-image)

· [Install with repository](#install-with-repository)

### Install via Docker image
Create a docker-compose file, which looks like this:
```yml
version: '3.7'

services:
  db:
    image: postgres:12.0-alpine
    environment:
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin
      - POSTGRES_DB=backend
    networks:
      - fridgify_production
  backend:
    image: fridgify/fridgify:latest
    ports:
      - <port-on-host>:9000
    volumes:
      - <static-files-path>:/fridgify/fridgify_backend/static/
      - <logs-path>:/fridgify/logs/
    depends_on:
      - db
    environment:
      - <env-variables>:<value>
    env_file:
      - <env-file>
    networks:
      - fridgify_production
volumes:
  postgres_data:
networks:
  fridgify_production:
```

**services** - define multiple services which should be build and run <br/>

**Database service - db**
* image - Postgres image <br/>
* environment - environment variables needed by Postgres
* networks - specify a network of containers

Fridgify uses a Postgres database for data persistence. Be sure to change up your database credentials. <br/>

For more information on the Postgres docker image, visit their [documentation](https://hub.docker.com/_/postgres).

**Backend service - backend**
* image - latest stable Fridgify image
* ports - port on your host (Fridgify uses port 9000 inside the container)
* volumes - persisted files on the host
  * static-files - swagger documentation
  * logs - Fridgify's logs
* depends_on - wait for the database container before running this container
* environment - declare some environment variables you
* env_file - declare an environment file, which contains environment variables
* networks - specify a network of containers

**volumes** - docker volumes
* postgres_data - postgres volume

**network** - define the network of containers

After saving the docker-compose file, execute it: `docker-compose up`

On your machine, the backend should be reachable on your defined port.

If you want to deploy to a server, make sure to create a proxy to that port as well as define the static files.

### Install with repository
Pull the repository and add your environment file in the root folder. Modify the *docker-compose.production.yml* to point to your environment file.

Run `docker-compose -f docker-compose.production.yml up --build` to build and run the docker container.

If you did not change the exposed ports, the backend should be reachable at port 9000. 
If you want to deploy to a server, make sure to create a proxy to that port as well as define the static files.

### Environment [](#env)
**ENV_FILE** - define your environment file, otherwise .empty is used (only for repository installation)<br/>

**Firebase Environments**

**FB_API_KEY** - API Key for Firebase<br/>
**FB_DL_URL** - BASE URL to Firebase Dynamic Link API<br/>
**GOOGLE_APPLICATION_CREDENTIALS** - path to your firebase key file<br/>

**hopper Environment**

**HP_APP** - path to your serialized hopper application<br/>
**LOGO** - URL to your logo

**Fridgify Environment**
**ANDROID_PN** - package name of your Android application<br/>
**IOS_BID** - name of your iOS bundle ID<br/>
**FRIDGIFY_DL_URL** - specify the dynamic link base url, your dynamic links should have<br/>
**DJANGO_SETTINGS_MODULE** - specify a module to use (for production: fridgify_backend.settings.production)

Look at the [.empty](./.empty)-file for an example environment file.