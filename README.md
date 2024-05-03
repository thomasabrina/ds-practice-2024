# Distributed Systems @ University of Tartu

This repository contains the code for the practice sessions of the Distributed Systems course at the University of Tartu, focusing on a distributed bookstore system.

## Getting Started

### Overview

The project consists of multiple services, each located in a separate folder:

- **Frontend Service**: Provides the user interface for the bookstore.
- **Orchestrator Service**: Coordinates between the frontend and various backend services.
- **Book Database Service**: Manages book data with operations like Read, Write, IncrementStock, and DecrementStock.
- **Order Executor Service**: Handles the execution of book orders.
- **Payment Service**: Manages payment transactions.
- **Fraud Detection Service**: Analyzes transactions to detect potential fraud.
- **Transaction Verification Service**: Verifies the legitimacy of transactions.
- **Suggestions Service**: Offers book recommendations based on user preferences.

Each service folder contains a Dockerfile, a `requirements.txt` file, and the source code of the service.

### Running the Code with Docker Compose [Recommended]

1. Clone this repository.
2. Ensure Docker and Docker Compose are installed.
3. Run the following command in the root folder of the repository:

`docker compose up`


This will start the system with the multiple services. Each service will be restarted automatically when you make changes to the code, so you don't have to restart the system manually while developing. If you want to know how the services are started and configured, check the `docker-compose.yaml` file.

The checkpoint evaluations will be done using the code that is started with Docker Compose, so make sure that your code works with Docker Compose.

If, for some reason, changes to the code are not reflected, try to force rebuilding the Docker images with the following command:

`docker compose up --build`


### Run the code locally

Even though you can run the code locally, it is recommended to use Docker and Docker Compose to run the code. This way you don't have to install any dependencies locally and you can easily run the code on any platform.

If you want to run the code locally, you need to install the following dependencies:

backend services:
- Python 3.8 or newer
- pip
- [grpcio-tools](https://grpc.io/docs/languages/python/quickstart/)
- requirements.txt dependencies from each service

frontend service:
- node.js, npm (or any other package manager)

And then run each service individually.
