# sre-platform-demo

A simple Flask app containerized with Docker to demonstrate basic SRE / DevOps skills.

## Features

- Python Flask service
- Dockerized app
- Health check endpoint

## Endpoints

- `/` - main service endpoint
- `/health` - health check endpoint

## Run locally with Docker

```bash
docker compose up --build