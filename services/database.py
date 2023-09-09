# Desc: Import the necesary libraries and modules to create the database services.
from sqlalchemy import not_

# Desc: Import components from my own modules to create the database services.
from schemas.database import DatabaseSchema
from models.database import DatabaseModel

# Desc:  Database services class.
class DatabaseServices:
    def __init__(self, db):
        self.db = db

    # Desc: Function to create a new database record.
    def create(self, database: DatabaseSchema):
        new_record = DatabaseModel(**database.model_dump())
        self.db.add(new_record)
        self.db.commit()
        self.db.refresh(new_record)
        return new_record

    # Desc: Function to get all the database records.
    def get_all(self):
        recods = self.db.query(DatabaseModel).all()
        return recods
    
    # Desc: Function to get a database record by TIN.
    def get_by_tin(self, tin: int):
        record = self.db.query(DatabaseModel).filter(DatabaseModel.tin == tin).first()
        return record
    
    # Desc: Function to get a database record by name.
    def get_by_name(self, name: str):
        record = self.db.query(DatabaseModel).filter(DatabaseModel.name == name).first()
        return record
    
    # Desc: Function to get a database record by last name.
    def get_by_last_name(self, last_name: str):
        record = self.db.query(DatabaseModel).filter(DatabaseModel.last_name == last_name).first()
        return record
    
    # Desc: Function to get a database record by email.
    def get_by_email(self, email: str):
        record = self.db.query(DatabaseModel).filter(DatabaseModel.email == email).first()
        return record
    
    # Desc: Function to update a database record by TIN.
    def update_by_tin(self, tin_to_search, database: DatabaseSchema):
        with self.db.begin() as transaction:
            recor_to_update = self.db.query(DatabaseModel).filter(DatabaseModel.tin == tin_to_search).first()
            if recor_to_update:
                record_data = database.model_dump()
                tin_check = self.db.query(DatabaseModel).filter(DatabaseModel.tin == record_data['tin'], not_(DatabaseModel.tin == tin_to_search)).first()
                email_check = self.db.query(DatabaseModel).filter(DatabaseModel.email == record_data['email'], not_(DatabaseModel.tin == tin_to_search)).first()
                if tin_check:
                    transaction.rollback()
                    return False
                if email_check:
                    transaction.rollback()
                    return False
                for key, value in record_data.items():
                    setattr(recor_to_update, key, value)
                transaction.commit()
                return True
            transaction.rollback()
            return None                
    
    # Desc: Function to eliminate a database record by TIN.
    def delete_by_tin(self, tin: int):
        with self.db.begin() as transaction:
            record = self.db.query(DatabaseModel).filter(DatabaseModel.tin == tin).first()
            if not record:
                transaction.rollback()
                return None
            self.db.delete(record)
            transaction.commit()
            return True