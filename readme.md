# Inventory Management System API

## Description
This is a backend API for an Inventory Management System built with Django Rest Framework. It allows users to register, log in, and manage inventory items with CRUD operations.

## Features
- User registration and authentication (JWT)
- CRUD operations for inventory items
- Redis caching for performance

## Installation

1. Clone the repository:
   '''bash
   git clone https://github.com/yourusername/inventory-management-system.git
   cd inventory-management-system
   '''

2. Set up a virtual environment and install dependencies:
   '''bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   '''

3. Set up your database and update the '.env' file with your configurations.

4. Run migrations:
   '''bash
   python manage.py migrate
   '''

5. Start the development server:
   '''bash
   python manage.py runserver
   '''

## API Endpoints

- Register User: 'POST register/'
- Login User: 'POST login/'
- Create Item: 'POST items/'
- Read Item: 'GET items/{sku}/'
- Update Item: 'PUT items/{sku}/'
- Delete Item: 'DELETE items/{sku}/'

## Running Tests
To run tests, use:
'''bash
python manage.py test
'''

