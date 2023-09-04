# Desc: Import the necessary libraries and modules to create the services for the database.
from sqlalchemy import not_
from models.database import DatabaseModel
from schemas.database import DatabaseSchema

# Desc: Create a class DatabaseService to manage the database.
class DatabaseService:
    def __init__(self, db) -> None:
        self.db = db

    # Desc: Function to get all the records from the database.
    def get_all_records(self):
        records_list = self.db.query(DatabaseModel).all()
        return records_list
    
    # Desc: Function to get a record by nit from the database.
    def get_record_by_nit(self, nit: int):
        return self.db.query(DatabaseModel).filter(DatabaseModel.nit == nit).first()
    
    # Desc: Function to get a record by name from the database.
    def get_record_by_name(self, name: str):
        return self.db.query(DatabaseModel).filter(DatabaseModel.name == name).first()
    
    # Desc: Function to get a record category from the database.
    def get_record_category(self, category: str):
        return self.db.query(DatabaseModel).filter(DatabaseModel.category == category).all()
        
    
    # Desc: Function to create a new record in the database.
    def create_record(self, database_schema: DatabaseSchema):
        new_record = DatabaseModel(**database_schema.model_dump())
        self.db.add(new_record)
        self.db.commit()
        return None
    
    # Desc: Function to update a record in the database.
    def update_record(self, nit: int, database_schema: DatabaseSchema):
        with self.db.begin() as transaction:
            record_to_update = self.db.query(DatabaseModel).filter(DatabaseModel.nit == nit).first()
            if record_to_update:
                record_data = database_schema.model_dump()
                comprobation_name = self.db.query(DatabaseModel).filter(DatabaseModel.name == record_data['name'], not_(DatabaseModel.nit == nit)).first()
                if comprobation_name:
                    transaction.rollback()
                    return False
                for key, value in record_data.items():
                    setattr(record_to_update, key, value)
                self.db.commit()
                return True
            else:
                transaction.rollback()
                return False
    
    # Desc: Function to eliminate a record from the database using the nit as parameter.
    def delete_record(self, nit: int):
        record_to_delet = self.db.query(DatabaseModel).filter(DatabaseModel.nit == nit).first()
        if record_to_delet:
            self.db.delete(record_to_delet)
            self.db.commit()
            return True
        else:
            return False
        
    # Desc: Funtion to delete all the records from the database.
    def delete_all_records(self):
        self.db.query(DatabaseModel).delete()
        self.db.commit()
        return None