# Desc: Import necessary libraries and modules to create the database schema.
from pydantic import BaseModel, Field
from typing import Optional

# Desc: Import components from my own modules to create the database schema.
from models.roles import Categories

# Desc: Create the database schema using the BaseModel class.
class DatabaseSchema(BaseModel):

    ref: int = Field(..., alias='ref')
    category: Categories = Field(..., alias='category - categoría')
    tin: int = Field(..., alias='TIN - NIT')
    dv: Optional[int] = Field(None, alias='DV')
    name: str = Field(..., alias='name - nombre')
    last_name: Optional[str] = Field(None, alias='last_name - apellido')
    self_retainer: bool = Field(..., alias='self-retainer - autoretenedor')
    ciium: int = Field(..., alias='CIIU main - CIIU principal')
    ciius: Optional[int] = Field(None, alias='CIIU secondary - CIIU secundario')
    ciiut: Optional[int] = Field(None, alias='CIIU tertiary - CIIU terciario')
    email: str = Field(..., alias='email - correo electrónico')
    phone_number: str = Field(..., alias='phone number - número de teléfono')
    city: str = Field(..., alias='city - ciudad')
    address: str = Field(..., alias='address - dirección')
    contact_name: Optional[str] = Field(None, alias='contact name - nombre de contacto')
    contact_number: Optional[str] = Field(None, alias='contact number - número de contacto')
    created_date: str = Field(..., alias='created date - fecha de creación')

    class Config:
        # Desc: Allow the ORM mode.
        orm_mode = True