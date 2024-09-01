# URL Shortener

A simple URL shortener service built with FastAPI and MongoDB. This application allows users to shorten URLs and retrieve the original URL using a short identifier.

## Features

- Shorten URLs
- Redirect to original URL using a short identifier
- Health check endpoint

## Badges

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI Version](https://img.shields.io/badge/fastapi-0.68.2-blue.svg)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/mongodb-4.4%2B-green.svg)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/docker-enabled-blue.svg)](https://www.docker.com/)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/url-shortener.git
    cd url-shortener
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file in the root directory and add your environment variables:**

    ```env
    DATABASE_URL=<your-db-url>
    DATABASE_NAME=url_shortener_db
    PORT=8000
    ```

## Usage

1. **Run the FastAPI application:**

    ```bash
    python main.py
    ```

2. **Access the API:**

    - **Health Check:** `GET /health-check/` - Check the status of the service.
    - **Shorten URL:** `POST /shorten/` - Request body should include `original_url`.
    - **Redirect URL:** `GET /{short_url}` - Redirects to the original URL.

3. **Docker:**

    Build and run the Docker container:

    ```bash
    docker build -t url-shortener .
    docker run -p 8000:8000 --env-file .env url-shortener
    ```

## Logging

Logs are configured to be written to a file named with the current date and rotated daily. Older logs are archived in zip files.

## Contributing

Feel free to open issues and pull requests to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.