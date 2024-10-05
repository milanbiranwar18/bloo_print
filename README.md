# bloo_print  (Inventory Management System)
Backend API for a Simple Inventory Management System using Django Rest Framework Project Assignment for First Round


## Overview

This is an Inventory Management System built using Django and Django REST Framework (DRF). It allows users to register, log in, and manage inventory items (CRUD operations). JWT-based authentication is implemented for secure user login.

## Features
- **User Authentication**: Register, Login, Logout using JWT tokens.
- **Inventory Management**: Create, Read, Update, Delete (CRUD) items in the inventory.
- **Secure API**: All operations are protected with JWT authentication.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.x installed.
- Django 3.x or higher installed.
- Django REST Framework installed.
- Django Simple JWT for authentication.
- A database like PostgreSQL.
  
## Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone https://github.com/milanbiranwar18/bloo_print.git
    cd bloo_print
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**: Create a `.env` file in the root directory and add the following details:
    ```env
    SECRET_KEY=your_secret_key
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
    ```

5. **Run migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser (for admin access)**:
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

8. **Access the application**:
    - Admin: `http://127.0.0.1:8000/admin/`
    - API: `http://127.0.0.1:8000/user/`

## API Documentation

### Authentication

1. **User Registration**:  
   Endpoint: `/user/user_registration/`  
   Method: `POST`  
   Example Request:
    ```json
    {
      "first_name": "milan",
      "last_name": "biranwar",
      "location": "Pune",
      "mobile_num": 1234567890,
      "email": "milan@example.com",
      "username": "milan",
      "password": "yourpassword"
    }
    ```
   Response: `201 Created`
    ```json
    {
      "message": "User registered successfully"
    }
    ```

2. **User Login**:  
   Endpoint: `/user/user_login/`  
   Method: `POST`  
   Example Request:
    ```json
    {
      "username": "milan",
      "password": "yourpassword"
    }
    ```
   Response: `200 OK`
    ```json
    {
      "access": "access_token",
      "refresh": "refresh_token"
    }
    ```

3. **User Logout**:  
   Endpoint: `/user/user_logout/`  
   Method: `POST`  
   Example Request:
    ```json
    {
      "refresh": "refresh_token"
    }
    ```
   Response: `205 Reset Content`
    ```json
    {
      "message": "Logout successfully"
    }
    ```

### Inventory Management

1. **Create Item**:  
   Endpoint: `/inventory/items/`  
   Method: `POST`  
   Example Request:
    ```json
    {
      "name": "Item1",
      "sku": "SKU001",
      "quantity": 100,
      "price": 50.0,
      "description": "Sample item description",
      "category": "Electronics"
    }
    ```
   Response: `201 Created`
    ```json
    {
      "Message": "Item created successfully",
      "data": { "id": 1, "name": "Item1", ... }
    }
    ```

2. **Get Item**:  
   Endpoint: `/inventory/items/<item_id>/`  
   Method: `GET`  
   Example Response:
    ```json
    {
      "data": {
        "id": 1,
        "name": "Item1",
        "sku": "SKU001",
        "quantity": 100,
        "price": 50.0,
        "description": "Sample item description",
        "category": "Electronics"
      }
    }
    ```

3. **Update Item**:  
   Endpoint: `/inventory/items/<item_id>/update/`  
   Method: `PUT`  
   Example Request:
    ```json
    {
      "name": "Updated Item",
      "sku": "UPDATEDSKU001",
      "quantity": 120,
      "price": 60.0,
      "description": "Updated item description",
      "category": "Updated Category"
    }
    ```
   Response: `200 OK`
    ```json
    {
      "Message": "Item updated successfully",
      "data": { "id": 1, "name": "Updated Item", ... }
    }
    ```

4. **Delete Item**:  
   Endpoint: `/inventory/items/<item_id>/delete/`  
   Method: `DELETE`  
   Response: `204 No Content`

## Usage Examples

1. **Register a new user**:
    ```bash
    curl -X POST http://127.0.0.1:8000/user/user_registration/ \
    -H "Content-Type: application/json" \
    -d '{"first_name": "milan", "last_name": "biranwar", "location": "Pune", "mobile_num": 1234567890, "email": "milan@example.com", "username": "milan", "password": "yourpassword"}'
    ```

2. **Login a user and obtain JWT tokens**:
    ```bash
    curl -X POST http://127.0.0.1:8000/user/user_login/ \
    -H "Content-Type: application/json" \
    -d '{"username": "milan", "password": "yourpassword"}'
    ```

3. **Create a new inventory item**:
    ```bash
    curl -X POST http://127.0.0.1:8000/inventory/items/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer <access_token>" \
    -d '{"name": "New Item", "sku": "NEW001", "quantity": 100, "price": 50.0, "description": "Sample item", "category": "Category1"}'
    ```

4. **Get an existing inventory item**:
    ```bash
    curl -X GET http://127.0.0.1:8000/inventory/items/1/ \
    -H "Authorization: Bearer <access_token>"
    ```

5. **Update an existing inventory item**:
    ```bash
    curl -X PUT http://127.0.0.1:8000/inventory/items/1/update/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer <access_token>" \
    -d '{"name": "Updated Item", "sku": "UPDATED001", "quantity": 200, "price": 100.0, "description": "Updated description", "category": "Updated Category"}'
    ```

6. **Delete an inventory item**:
    ```bash
    curl -X DELETE http://127.0.0.1:8000/inventory/items/1/delete/ \
    -H "Authorization: Bearer <access_token>"
    ```

## Running Unit Tests

To run unit tests, execute the following command:

```bash
python manage.py test

