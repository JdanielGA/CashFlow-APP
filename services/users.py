# Desc: Import the necessary libraries and modules to create the user services.
from sqlalchemy import not_
from models.users import UsersModel
from schemas.users import UsersSchema

# Desc: Create a class to manage the users services.
class UserService:
    def __init__(self, db) -> None:
        self.db = db

    # Desc: Create a funtion to get all the users.
    def get_all_users(self):
        users_list = self.db.query(UsersModel).all()
        return users_list
    
    # Desc: Create a funtion to get a user by id.
    def get_user_by_id(self, id: int):
        user = self.db.query(UsersModel).filter(UsersModel.id == id).first()
        return user
    
    # Desc: Create a funtion to get a user by company id.
    def get_user_by_company_id(self, company_id: int):
        user = self.db.query(UsersModel).filter(UsersModel.company_id == company_id).first()
        return user
    
    # Desc: Create a funtion to create a new user implementing the password hash with the set_password funtion from the model.
    def create_user(self, user: UsersSchema):
        new_user = UsersModel(
            company_id=user.company_id,
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            position=user.position,
            company_phone=user.company_phone,
            corporate_email=user.corporate_email,
            permission_level=user.permission_level
        )
        new_user.set_password(user.password_hash)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    # Desc: Create a funtion to update a user by company id checking if the user possible id already exists.
    def update_user(self, company_id: int, user: UsersSchema):
        with self.db.begin() as transaction:
            user_to_update = self.db.query(UsersModel).filter(UsersModel.company_id == company_id).first()
            if user_to_update:
                user_data = user.model_dump()
                comprobation_id = self.db.query(UsersModel).filter(UsersModel.id == user_data['id'],not_(UsersModel.company_id == user_data['company_id'])).first()
                if comprobation_id:
                    transaction.rollback()
                    return False
                for key, value in user_data.items():
                    setattr(user_to_update, key, value)
                self.db.commit()
                return True
            else:
                transaction.rollback()
                return False
            
    # Desc: Create a funtion to delete a user by company id.
    def delete_user(self, company_id: int):
        with self.db.begin() as transaction:
            user_to_delete = self.db.query(UsersModel).filter(UsersModel.company_id == company_id).first()
            if user_to_delete:
                self.db.delete(user_to_delete)
                self.db.commit()
                return True
            else:
                transaction.rollback()
                return False