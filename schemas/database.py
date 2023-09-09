# Desc: Import necessary libraries and modules to create the database schema.
from pydantic import BaseModel, Field
from typing import Optional

# Desc: Import components from my own modules to create the database schema.
from models.roles import Categories

# Desc: Create the database schema using the BaseModel class.
class DatabaseSchema(BaseModel):

    category: Categories = Field(..., alias='category')
    tin: int = Field(..., alias='tin')
    dv: Optional[int] = Field(None, alias='dv')
    name: str = Field(..., alias='name')
    last_name: Optional[str] = Field(None, alias='last_name')
    self_retainer: bool = Field(..., alias='self_retainer')
    ciium: int = Field(..., alias='ciium')
    ciius: Optional[int] = Field(None, alias='ciius')
    ciiut: Optional[int] = Field(None, alias='ciiut')
    email: str = Field(..., alias='email')
    phone_number: str = Field(..., alias='phone_number')
    city: str = Field(..., alias='city')
    address: str = Field(..., alias='address')
    contact_name: Optional[str] = Field(None, alias='contact_name')
    contact_number: Optional[str] = Field(None, alias='contact_number')
    created_date: str = Field(..., alias='created_date')

    class Config:
        # Desc: Allow the ORM mode.
        orm_mode = True

# Desc: Create the database update schema using the BaseModel class.
class UpdateSchema(BaseModel):

    category: Categories = Field(..., alias='category')
    tin: int = Field(..., alias='tin')
    dv: Optional[int] = Field(None, alias='dv')
    name: str = Field(..., alias='name')
    last_name: Optional[str] = Field(None, alias='last_name')
    self_retainer: bool = Field(..., alias='self_retainer')
    ciium: int = Field(..., alias='ciium')
    ciius: Optional[int] = Field(None, alias='ciius')
    ciiut: Optional[int] = Field(None, alias='ciiut')
    email: str = Field(..., alias='email')
    phone_number: str = Field(..., alias='phone_number')
    city: str = Field(..., alias='city')
    address: str = Field(..., alias='address')
    contact_name: Optional[str] = Field(None, alias='contact_name')
    contact_number: Optional[str] = Field(None, alias='contact_number')

    class Config:
        # Desc: Allow the ORM mode.
        orm_mode = True