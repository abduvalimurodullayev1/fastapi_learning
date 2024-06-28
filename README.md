# FastAPI Learning Project

This project is a learning resource for building an API with FastAPI. It includes user authentication, product management, and GitHub OAuth integration.

## Features

- **User Authentication**: Sign up and login functionality with JWT-based authentication.
- **Product Management**: CRUD operations for products.
- **GitHub OAuth**: Login using GitHub OAuth.

## Technologies Used

- FastAPI
- SQLAlchemy
- Pydantic
- Passlib
- JWT
- HTTPX
- Dotenv

## Setup

### Prerequisites

- Python 3.10+
- Virtual environment (recommended)

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/abduvalimurodullayev1/fastapi_learning.git
    cd fastapi_learning
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file** in the root directory and add your GitHub client ID and secret:
    ```
    github_client_id=<your_github_client_id>
    github_secret_id=<your_github_secret_id>
    ```

5. **Run the application**:
    ```bash
    uvicorn main:app --reload
    ```

## API Endpoints

### User Endpoints

- **Signup**: `POST /signup`
    - Request body: `{"email": "user@example.com", "password": "yourpassword"}`
    - Response: JWT token

- **Login**: `POST /login`
    - Request body: `{"email": "user@example.com", "password": "yourpassword"}`
    - Response: JWT token

- **GitHub Login Redirect**: `GET /login_github`
    - Redirects to GitHub OAuth page

- **GitHub Code Exchange**: `GET /github-code?code=<code>`
    - Exchanges the code for an access token and retrieves user info

### Product Endpoints

- **Get All Products**: `GET /products`
    - Response: List of products

- **Get Product by ID**: `GET /products/{id}`
    - Path parameter: `id` (product ID)
    - Response: Product details

- **Add Product**: `POST /products`
    - Request body: `{"title": "Product Title", "description": "Product Description", "price": 100}`
    - Response: Success message
    - Requires JWT token in header

## Project Structure

- **main.py**: Main application file with FastAPI routes
- **models.py**: SQLAlchemy models for User and Product
- **schemas.py**: Pydantic schemas for request and response validation
- **config.py**: Database configuration
- **jwt_bearer.py**: JWT authentication dependency
- **jwt_handler.py**: JWT token generation and validation
- **requirements.txt**: List of dependencies

## Running Tests

To run the tests, you need to have `pytest` installed. You can run the tests using the following command:

```bash
pytest
