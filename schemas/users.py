# Desc: Import necessary libraries and modules to create the user schema.
from pydantic import BaseModel, Field
from typing import Optional

# Desc: Import components from my own modules to create the user schema.
from models.roles import Roles

# Desc: Create the user schema using the BaseModel class.
class UserSchema(BaseModel):

    id_number: int = Field(..., alias='id_number')
    company_id: str = Field(..., alias='company_id')
    first_name: str = Field(..., alias='first_name')
    last_name: str = Field(..., alias='last_name')
    position: str = Field(..., alias='position')
    email: str = Field(..., alias='email')
    password: Optional[str] = Field(None, alias='password')
    role: Roles = Field(..., alias='role')
    active_status: bool = Field(..., alias='active_status')
    date_created: str = Field(..., alias='date_created')

    class Config:
        # Desc: Allow the ORM mode.
        orm_mode = True

# Desc: Create the user update schema using the BaseModel class.
class UserUpdateSchema(BaseModel):
    
    id_number: int = Field(..., alias='id_number')
    company_id: str = Field(..., alias='company_id')
    first_name: str = Field(..., alias='first_name')
    last_name: str = Field(..., alias='last_name')
    position: str = Field(..., alias='position')
    email: str = Field(..., alias='email')
    role: Roles = Field(..., alias='role')
    active_status: bool = Field(..., alias='active_status')

    class Config:
        # Desc: Allow the ORM mode.
        orm_mode = True

# Desc: Create the password update schema using the BaseModel class.
class PasswordUpdateSchema(BaseModel):

    email: str = Field(..., alias='email')
    old_password: str = Field(..., alias='old_password')
    password: str = Field(..., alias='new_password')

    class Config:
        # Desc: Allow the ORM mode.
        orm_mode = True