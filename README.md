# WWII Mission Data Normalization Project

## Overview

This project is designed to normalize and manage World War II mission data stored in a PostgreSQL database. The project implements a Flask web application that interacts with normalized tables via SQLAlchemy ORM, providing endpoints for viewing and managing mission and target data.

### Key Features
- **Data Normalization:** 
  Normalizes WWII mission data from a flat structure into a relational database model, including tables for missions, targets, countries, cities, industries, and target types.
  
- **RESTful API Endpoints:** 
  Provides endpoints to retrieve and manage missions and target data in JSON format.

- **Efficient Querying:** 
  Optimizes database queries using appropriate indexing and performance tuning with `EXPLAIN ANALYZE`.

## Database Schema

### Normalized Tables
1. **Mission**: Stores core information about each mission, such as date, air force, target, etc.
2. **Target**: Stores information about targets, including coordinates, priority, and relationships to cities and industries.
3. **City**: Stores city names and country associations.
4. **Country**: Stores country names.
5. **Target Industry**: Stores types of industries affected by missions.
6. **Target Type**: Stores types of targets.

### Key Relationships
- **Mission ↔ Target**: Each mission is associated with one target.
- **Target ↔ City**: Each target is associated with one city.
- **City ↔ Country**: Each city is associated with one country.

## Endpoints

### Mission Endpoints
- **GET /api/mission**: Retrieve all missions with relevant details such as air force, mission date, and target information.
- **GET /api/mission/{id}**: Retrieve a specific mission by its ID.
- **POST /api/mission**: Create a new mission (requires data in JSON format).
- **PUT /api/mission/{id}**: Update an existing mission by ID.
- **DELETE /api/mission/{id}**: Delete a mission by ID.

### Target Endpoints
- **GET /api/target**: Retrieve all target data.
- **POST /api/target**: Create a new target entry.
- **PUT /api/target/{id}**: Update an existing target by ID.
- **DELETE /api/target/{id}**: Delete a target by ID.

## How to Run

### Prerequisites
- **Python 3.8+**
- **PostgreSQL**
- **SQLAlchemy ORM**
- **Flask**

### Setup

1. **Clone the Repository**
    ```bash
    git clone <repo-url>
    cd normolize_data
    ```

2. **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Database**
    - Create a PostgreSQL database named `wwii_missions`.
    - Update the database configuration in the `config.py` file.

5. **Run Database Migrations**
    ```bash
    python manage.py db upgrade
    ```

6. **Run the Application**
    ```bash
    python main.py
    ```

7. **Access the Application**
   Open [http://localhost:5000](http://localhost:5000) in your browser.

### Seeding the Database
To seed the database with initial normalized data from the `mission` table:
```bash
python seed.py
