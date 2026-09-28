# Digital Lost & Found REST API

## 1. Project Description

The Digital Lost & Found REST API is a FastAPI-based application for managing lost and found items in a college.

Students can report lost or found items and manage item information through REST APIs. The application stores all item data in a SQLite database using SQLModel.

The API supports creating, viewing, updating, deleting, and filtering items by status and category.

## 2. Technologies Used

* Python
* FastAPI
* SQLModel
* SQLite
* Pydantic
* Uvicorn
* Swagger UI

## 3. Installation Steps

### Step 1: Clone the repository

```bash
git clone https://github.com/kajal836877/LostFoundAPI.git
```

### Step 2: Open the project folder

```bash
cd LostFoundAPI
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

### Step 4: Activate the virtual environment

For Windows:

```bash
venv\Scripts\activate
```

### Step 5: Install required packages

```bash
pip install -r requirements.txt
```

## 4. Command to Run the FastAPI Application

Run the following command in the terminal:

```bash
uvicorn main:app --reload
```

## 5. Swagger UI URL

After starting the application, open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test all the available API endpoints.

## 6. Available API Endpoints

| Method | Endpoint                     | Description                    |
| ------ | ---------------------------- | ------------------------------ |
| POST   | `/items`                     | Create a new lost/found item   |
| GET    | `/items`                     | Get all items                  |
| GET    | `/items/{item_id}`           | Get a specific item by ID      |
| PUT    | `/items/{item_id}`           | Update an existing item        |
| DELETE | `/items/{item_id}`           | Delete an item                 |
| GET    | `/items/status/{status}`     | Get items filtered by status   |
| GET    | `/items/category/{category}` | Get items filtered by category |

### Status Values

The API accepts only these status values:

* `Lost`
* `Found`
* `Returned`

## 7. Validation and Error Handling

The API validates required fields such as title, description, category, location, and reported_by.

The description must contain meaningful text, and the status must be one of `Lost`, `Found`, or `Returned`.

If an item does not exist, the API returns a `404` error.

Invalid request data is handled by FastAPI validation and returns an appropriate `422` response.

## 8. Database

The application uses SQLite for data storage.

The database table is automatically created when the FastAPI application starts.

SQLModel is used to define the database model and perform database operations.

## 9. Screenshots

The project includes screenshots demonstrating:

* POST `/items`
* GET `/items`
* GET `/items/{item_id}`
* PUT `/items/{item_id}`
* DELETE `/items/{item_id}`
* GET `/items/status/{status}`
* GET `/items/category/{category}`
* Invalid request with FastAPI validation/error response

The screenshots show the API endpoint, request data, and response returned by the API.
