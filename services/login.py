# Desc: Import the necessary libraries and modules to create the login services.
from werkzeug.security import check_password_hash
from models.users import UsersModel

# Desc: Create a class to manage the login services using the database users information.
class LoginService:
    def __init__(self, db) -> None:
        self.db = db

    # Desc: Create a funtion for the login process.
    def login(self, email: str, password: str):
        user = self.db.query(UsersModel).filter(UsersModel.corporate_email == email).first()
        if user:
            if check_password_hash(user.password_hash, password):
                return user
            else:
                return False
        else:
            return False