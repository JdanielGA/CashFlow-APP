# Desc: Import the necessary libraries and modules to create the users schema.
from pydantic import BaseModel, Field
from typing import Optional

# Desc: Create the users schema with the necessary fields using the BaseModel class.
class UsersSchema(BaseModel):

    company_id: int = Field(default=0)
    id: int = Field(default=0)
    first_name: str = Field(default='', min_length=1, max_length=50)
    last_name: str = Field(default='', min_length=1, max_length=50)
    position: str = Field(default='Position', min_length=1, max_length=50)
    company_phone: int = Field(default=0)
    corporate_email: str = Field(default='position@company.com', min_length=1, max_length=50)
    password_hash: Optional[str] = Field(default='password_hash', min_length=1, max_length=255)
    status: bool = Field(default=True)