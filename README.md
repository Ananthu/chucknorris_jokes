# Chuck Norris Jokes API

This repository contains the Dockerized Flask application for a Chuck Norris Jokes API, which allows users to search, create, update, and delete Chuck Norris jokes.

## Getting Started

These instructions will cover usage information and for the docker container 

### Prerequisites

In order to run this container you'll need docker installed.

- [Windows](https://docs.docker.com/windows/started)
- [OS X](https://docs.docker.com/mac/started/)
- [Linux](https://docs.docker.com/linux/started/)

### Installing

#### Pull the Docker Image

You can pull the image from Docker Hub using the following command:

```bash
docker pull ananthu10/chuck_norris_jokes
```
Run the app using the following commands:

```bash
docker run -d -p 5000:5000 yananthu10/chuck_norris_jokes:latest
```


# API ENDPOINTS
The API supports the following endpoints:
```
GET /api/jokes/: List all jokes.
POST /api/jokes/: Create a new joke.
GET /api/jokes/{id}: Retrieve a joke by ID.
PUT /api/jokes/{id}: Update a joke by ID.
DELETE /api/jokes/{id}: Delete a joke by ID.
```