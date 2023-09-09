# Desc: Import the necessary libraries and modules to create roles.
from enum import Enum

# Desc: Create the roles list class.
class Roles(Enum):
    ADMIN = 'Admin'
    USER = 'User'
    GUEST = 'Guest'

# Desc: Create the categories list class.
class Categories(Enum):
    EMPLOYEE = 'Employee'
    CLIENT = 'Client'
    SUPPLIER = 'Supplier'
    COMPANY = 'Company'