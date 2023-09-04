# Desc: Import the necessary libraries and modules to create the database schema.
from pydantic import BaseModel, Field
from typing import Optional


# Desc: Create the database schema with the necessary fields using the BaseModel class.
class DatabaseSchema(BaseModel):

    category: str = Field(default='Cliente')
    nit: int = Field(default=0)
    dv: int = Field(default=0)
    name: str = Field(default='Razón Social', min_length=1, max_length=50)
    city: str = Field(default='Bogotá D.C.', min_length=1, max_length=50)
    adress: str = Field(default='Cll. 1 #1 - 1, ofi 101', min_length=1, max_length=255)
    email: str = Field(default='email@compañia.com', min_length=1, max_length=50)
    number: int = Field(default=0)
    self_retainer: bool = Field(default=False)
    main_activity: int = Field(default=0)
    second_activity: Optional[int] = Field(default=0)
    third_activity: Optional[int] = Field(default=0)
    contac_name: Optional[str] = Field(default='Nombre de Contacto', max_length=50)
    contac_number: Optional[int] = Field(default=0)