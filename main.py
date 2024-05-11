from fastapi import FastAPI, Depends, Path
from pydantic import BaseModel, Field
from typing import Any, List

# Step 1: Read the configuration file to determine the fields for the request model


# Step 2: Dynamically generate the Pydantic model based on the configuration data
from typing import Dict, Type


def create_dynamic_model(
    model_name: str, fields: Dict[str, Type[Any]]
) -> Type[BaseModel]:
    """
    Dynamically creates a Pydantic model.

    Args:
    model_name (str): The name of the model.
    fields (Dict[str, Type]): A dictionary with field names as keys and their types and default values as values.

    Returns:
    Type[BaseModel]: A new Pydantic model class.
    """
    # Create a new dictionary to hold field attributes and annotations
    attributes = {"__annotations__": {}}
    for field_name, field_type in fields.items():
        # Set the type annotation for each field
        attributes["__annotations__"][field_name] = field_type
        # Use Field(...) to define the field with defaults and possibly other configurations
        attributes[field_name] = Field(...)

    # Create a new Pydantic BaseModel class
    dynamic_model = type(model_name, (BaseModel,), attributes)

    return dynamic_model


# Step 4: Implement the dynamic route generation logic using the dynamically generated Pydantic model
app = FastAPI()

# Dynamic route generation based on configuration file
for route_info in [
    {"path": "/api/v1/{name}", "methods": ["GET"]},
    {"path": "/api/v2?id={id}", "methods": ["POST"]},
]:
    route_path = route_info["path"]
    # Define the fields and their types
    fields = (
        {
            "name": str,
        }
        if route_info["methods"] == ["GET"]
        else {
            "id": int,
        }
    )

    # Create the dynamic model
    MyNewClass = create_dynamic_model("MyNewClass", fields)

    # Step 3: Create a custom dependency for request data validation
    def validate_request_data(request_data: MyNewClass = Depends()):
        # Additional validation logic can be added here if needed
        return request_data

    @app.get(route_path)
    async def generic_handler(
        request_data: MyNewClass = Depends(validate_request_data),
    ):
        # Your generic handler logic here
        return {"message": "Route processed successfully"}
