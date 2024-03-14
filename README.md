# Fast API Application

This repository contains a Fast API application with Docker, Docker Compose, and Alembic for managing database migrations.

## Installation

1. Make sure Docker is installed and running on your system.

2. Clone this repository:
    ```bash
    git clone https://github.com/khersinpro/fast-social-media
    cd fast-api-app
    ```

3. Build the Docker image:
    ```bash
    docker build -t fast_api_app -f dockerfile.dev .
    ```

4. Start the containers using Docker Compose:
    ```bash
    docker-compose -f docker-compose.dev.yml up -d
    ```

5. Apply database migrations and seeders with Alembic:
    ```bash
    alembic upgrade head
    ```
    
## Usage
Once the containers are started, you can access the Fast API application at the following address: `http://localhost:8000`

## Project Structure
- `app/`: Contains the code for the Fast API application.
  - `app/api/`: Directory for API-related code.
    - `models/`: Contains the alembic models for the API.
    - `routes/`: Contains the route definitions for the API.
    - `schemas/`: Contains the Pydantic schemas for the API.
    - `security/`: Contains security-related code for the API.
- `alembic/`: Directory containing database migrations.
- `dockerfile.dev`: Dockerfile for the development environment.
- `docker-compose.dev.yml`: Docker Compose configuration file for the development environment.
- `requirements.txt`: File containing Python dependencies.







