# Desc: Import the necessary libraries and modules to create roles.
from enum import Enum

# Desc: Create the roles list class.
class Roles(Enum):
    ADMIN = 'Admin'
    USER = 'User'
    GUEST = 'Guest'