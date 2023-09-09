# Desc: Import the necessary libraries and modules to create the user services.
from sqlalchemy import not_

# Desc: Import components from my own modules to create the user services.
from models.users import UserModel
from schemas.users import UserSchema

# Desc: Class user to manage the services.
class UserService:
    def __init__(self, db):
        self.db = db

    # Desc: Function to get all users.
    def get_all_users(self):
        users = self.db.query(UserModel).all()
        return users
    
    # Desc: Function to get a user by ID number.
    def get_user_by_id_number(self, id_number: int):
        user = self.db.query(UserModel).filter(UserModel.id_number == id_number).first()
        return user
    
    # Desc: Function to get a user by company ID.
    def get_user_by_company_id(self, company_id: str):
        user = self.db.query(UserModel).filter(UserModel.company_id == company_id).first()
        return user
    
    # Desc: Function to get a user by email.
    def get_user_by_email(self, email: str):
        user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return user
    
    # Desc: Function to create a new user using password hash.
    def create_user(self, user: UserSchema):
        new_user = UserModel(**user.model_dump())
        new_user.generate_password(user.password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    # Desc: Function to update a user.
    def update_user(self, id_to_search: int, user: UserSchema):
        with self.db.begin() as transaction:
            user_to_update = self.db.query(UserModel).filter(UserModel.id_number == id_to_search).first()
            if user_to_update:
                user_data = user.model_dump()
                verification_company_id = self.db.query(UserModel).filter(UserModel.company_id == user_data['company_id'], not_(UserModel.id_number == id_to_search)).first()
                verification_email = self.db.query(UserModel).filter(UserModel.email == user_data['email'], not_(UserModel.id_number == id_to_search)).first()
                if verification_company_id:
                    transaction.rollback()
                    return False
                if verification_email:
                    transaction.rollback()
                    return False
                for key, value in user_data.items():
                    setattr(user_to_update, key, value)
                self.db.commit()
                return True
            else:
                transaction.rollback()
                return None
            
    # Desc: Function to update a user password.
    def update_user_password(self, email: str, old_password: str, new_password: str):
        with self.db.begin() as transaction:
            user_to_update = self.db.query(UserModel).filter(UserModel.email == email).first()
            if user_to_update:
                if user_to_update.check_password(old_password):
                    user_to_update.generate_password(new_password)
                    self.db.commit()
                    return True
                else:
                    transaction.rollback()
                    return False
            else:
                transaction.rollback()
                return None
            
    # Desc: Function to delete a user.
    def delete_user(self, id_number: int):
        with self.db.begin() as transaction:
            user_to_delete = self.db.query(UserModel).filter(UserModel.id_number == id_number).first()
            if user_to_delete:
                self.db.delete(user_to_delete)
                self.db.commit()
                return True
            else:
                transaction.rollback()
                return None
    
    # Desc: Function to login a user.
    def login_user(self, email: str, password: str):
        user = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            return None
        if not user.check_password(password):
            return None
        return user