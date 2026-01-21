# API-SUT (API System Under Test)

A demonstration CRUD API built with Python and FastAPI, designed for QA Engineers to practice API testing. This API uses an in-memory data store with pre-loaded demo data, making it perfect for testing and portfolio demonstrations.

## Features

- **Full CRUD Operations**: Create, Read, Update, Delete endpoints
- **In-Memory Data Store**: No database setup required
- **Pre-loaded Demo Data**: 5 sample items ready for testing
- **Swagger Documentation**: Interactive API docs at `/docs`
- **Proper HTTP Status Codes**: Industry-standard responses
- **Input Validation**: Pydantic models ensure data integrity
- **Azure App Service Ready**: Compatible with Azure deployment

## Requirements

- Python 3.11+ (Azure App Service compatible)
- FastAPI
- Uvicorn

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/api-sut.git
   cd api-sut
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

Start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

Once running, access the interactive Swagger documentation at:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| GET | `/` | Welcome message | 200 OK |
| GET | `/health` | Health check | 200 OK |
| GET | `/items` | Get all items | 200 OK |
| GET | `/items/{id}` | Get item by ID | 200 OK / 404 Not Found |
| POST | `/items` | Create new item | 201 Created |
| PUT | `/items/{id}` | Update item | 200 OK / 404 Not Found |
| DELETE | `/items/{id}` | Delete item | 204 No Content / 404 Not Found |

## Data Model

### Item

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | auto | Unique identifier (system-generated) |
| name | string | yes | Item name (1-100 characters) |
| description | string | no | Item description (max 500 characters) |
| price | float | yes | Item price (must be > 0) |
| quantity | integer | yes | Available quantity (must be >= 0) |
| created_at | datetime | auto | Creation timestamp (system-generated) |
| updated_at | datetime | auto | Last update timestamp (system-generated) |

## Example Requests

### Get All Items
```bash
curl -X GET http://127.0.0.1:8000/items
```

### Get Item by ID
```bash
curl -X GET http://127.0.0.1:8000/items/1
```

### Create Item
```bash
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "New Item", "description": "A test item", "price": 19.99, "quantity": 10}'
```

### Update Item
```bash
curl -X PUT http://127.0.0.1:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Item", "description": "Updated description", "price": 24.99, "quantity": 5}'
```

### Delete Item
```bash
curl -X DELETE http://127.0.0.1:8000/items/1
```

## Demo Data

The API comes pre-loaded with 5 demo items:

1. **Wireless Mouse** - $29.99 (150 in stock)
2. **Mechanical Keyboard** - $149.99 (75 in stock)
3. **USB-C Hub** - $49.99 (200 in stock)
4. **Monitor Stand** - $79.99 (50 in stock)
5. **Webcam HD** - $89.99 (120 in stock)

## Deployment to Azure App Service

### Prerequisites
- Azure CLI installed
- Azure subscription

### Deployment Steps

1. Create a `startup.txt` file (already included):
   ```
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   ```

2. Deploy using Azure CLI:
   ```bash
   az webapp up --name api-sut --runtime "PYTHON:3.11" --sku B1
   ```

3. Configure the startup command in Azure Portal or via CLI:
   ```bash
   az webapp config set --name api-sut --resource-group <your-resource-group> --startup-file "gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app"
   ```

## Testing Scenarios

This API is perfect for practicing:

- **Positive Testing**: Valid CRUD operations
- **Negative Testing**: Invalid IDs, missing fields, invalid data types
- **Boundary Testing**: Min/max values for fields
- **Status Code Validation**: Verify correct HTTP responses
- **Response Schema Validation**: Validate JSON structure
- **Performance Testing**: Load testing with tools like k6 or JMeter

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
