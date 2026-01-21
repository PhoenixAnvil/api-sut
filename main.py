"""
API-SUT: A simple CRUD API for QA Engineer portfolio demonstrations.

This API provides a complete set of CRUD operations using an in-memory data store,
making it perfect for testing and demonstration purposes without requiring a database.
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, StrictFloat, StrictInt
from typing import Optional
from datetime import datetime

# Initialize FastAPI application with metadata for Swagger docs
app = FastAPI(
    title="API-SUT",
    description="""
## API System Under Test

A demonstration CRUD API designed for QA Engineers to practice API testing.

### Features
- **In-Memory Data Store**: No database required
- **Pre-loaded Demo Data**: Start testing immediately
- **Full CRUD Operations**: Create, Read, Update, Delete
- **Proper HTTP Status Codes**: Industry-standard responses

### Use Cases
- API Testing Practice
- Test Automation Development
- CI/CD Pipeline Testing
- Portfolio Demonstrations
    """,
    version="1.0.0",
    contact={
        "name": "API-SUT Support",
        "url": "https://github.com/your-username/api-sut",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)


# Pydantic models for request/response validation
class ItemBase(BaseModel):
    """Base model with common item attributes."""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the item")
    description: Optional[str] = Field(None, max_length=500, description="Optional description")
    price: StrictFloat = Field(..., gt=0, description="Price of the item (must be greater than 0)")
    quantity: StrictInt = Field(..., ge=0, description="Available quantity (must be 0 or greater)")


class ItemCreate(ItemBase):
    """Model for creating a new item."""
    pass


class ItemUpdate(ItemBase):
    """Model for updating an existing item."""
    pass


class Item(ItemBase):
    """Complete item model including system-generated fields."""
    id: int = Field(..., description="Unique identifier for the item")
    created_at: datetime = Field(..., description="Timestamp when the item was created")
    updated_at: datetime = Field(..., description="Timestamp when the item was last updated")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Widget",
                "description": "A useful widget",
                "price": 29.99,
                "quantity": 100,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }


class MessageResponse(BaseModel):
    """Standard message response model."""
    message: str = Field(..., description="Response message")


# In-memory data store
data_store: dict[int, dict] = {}
next_id: int = 1


def initialize_demo_data():
    """Initialize the data store with demo data."""
    global next_id
    
    demo_items = [
        {
            "name": "Wireless Mouse",
            "description": "Ergonomic wireless mouse with adjustable DPI",
            "price": 29.99,
            "quantity": 150
        },
        {
            "name": "Mechanical Keyboard",
            "description": "RGB mechanical keyboard with Cherry MX switches",
            "price": 149.99,
            "quantity": 75
        },
        {
            "name": "USB-C Hub",
            "description": "7-in-1 USB-C hub with HDMI, USB 3.0, and SD card reader",
            "price": 49.99,
            "quantity": 200
        },
        {
            "name": "Monitor Stand",
            "description": "Adjustable monitor stand with cable management",
            "price": 79.99,
            "quantity": 50
        },
        {
            "name": "Webcam HD",
            "description": "1080p HD webcam with built-in microphone",
            "price": 89.99,
            "quantity": 120
        }
    ]
    
    for item_data in demo_items:
        now = datetime.now()
        data_store[next_id] = {
            "id": next_id,
            **item_data,
            "created_at": now,
            "updated_at": now
        }
        next_id += 1


# Initialize demo data on startup
initialize_demo_data()


# API Endpoints

@app.get(
    "/items",
    response_model=list[Item],
    status_code=status.HTTP_200_OK,
    summary="Get all items",
    description="Retrieve a list of all items in the data store.",
    tags=["Items"]
)
def get_all_items():
    """
    Retrieve all items from the in-memory data store.
    
    Returns a list of all items with their complete details.
    """
    return list(data_store.values())


@app.get(
    "/items/{item_id}",
    response_model=Item,
    status_code=status.HTTP_200_OK,
    summary="Get item by ID",
    description="Retrieve a specific item by its unique identifier.",
    tags=["Items"],
    responses={
        404: {
            "description": "Item not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Item with id 999 not found"}
                }
            }
        }
    }
)
def get_item_by_id(item_id: int):
    """
    Retrieve a specific item by ID.
    
    - **item_id**: The unique identifier of the item to retrieve
    
    Raises HTTPException 404 if the item is not found.
    """
    if item_id not in data_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return data_store[item_id]


@app.post(
    "/items",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
    description="Create a new item in the data store.",
    tags=["Items"]
)
def create_item(item: ItemCreate):
    """
    Create a new item.
    
    - **name**: Name of the item (required)
    - **description**: Optional description
    - **price**: Price of the item (must be > 0)
    - **quantity**: Available quantity (must be >= 0)
    
    Returns the created item with its assigned ID and timestamps.
    """
    global next_id
    
    now = datetime.now()
    new_item = {
        "id": next_id,
        **item.model_dump(),
        "created_at": now,
        "updated_at": now
    }
    
    data_store[next_id] = new_item
    next_id += 1
    
    return new_item


@app.put(
    "/items/{item_id}",
    response_model=Item,
    status_code=status.HTTP_200_OK,
    summary="Update an item",
    description="Update an existing item by its ID. All fields must be provided.",
    tags=["Items"],
    responses={
        404: {
            "description": "Item not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Item with id 999 not found"}
                }
            }
        }
    }
)
def update_item(item_id: int, item: ItemUpdate):
    """
    Update an existing item (full replacement).
    
    - **item_id**: The unique identifier of the item to update
    - **name**: Name of the item (required)
    - **description**: Optional description
    - **price**: Price of the item (must be > 0)
    - **quantity**: Available quantity (must be >= 0)
    
    Raises HTTPException 404 if the item is not found.
    """
    if item_id not in data_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    existing_item = data_store[item_id]
    updated_item = {
        "id": item_id,
        **item.model_dump(),
        "created_at": existing_item["created_at"],
        "updated_at": datetime.now()
    }
    
    data_store[item_id] = updated_item
    return updated_item


@app.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
    description="Delete an item from the data store by its ID.",
    tags=["Items"],
    responses={
        404: {
            "description": "Item not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Item with id 999 not found"}
                }
            }
        }
    }
)
def delete_item(item_id: int):
    """
    Delete an item by ID.
    
    - **item_id**: The unique identifier of the item to delete
    
    Returns 204 No Content on success.
    Raises HTTPException 404 if the item is not found.
    """
    if item_id not in data_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    del data_store[item_id]
    return None


# Health check endpoint
@app.get(
    "/health",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check if the API is running.",
    tags=["Health"]
)
def health_check():
    """
    Health check endpoint.
    
    Returns a simple message indicating the API is operational.
    """
    return {"message": "API-SUT is healthy and running!"}


# Root endpoint
@app.get(
    "/",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Root endpoint",
    description="Welcome message and API information.",
    tags=["Health"]
)
def root():
    """
    Root endpoint with welcome message.
    
    Provides basic information about the API and links to documentation.
    """
    return {"message": "Welcome to API-SUT! Visit /docs for Swagger documentation."}
