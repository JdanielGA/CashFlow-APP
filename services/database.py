# Desc: Import the necessary libraries and modules to create the services for the database.
from fastapi import HTTPException
from models.database import DatabaseModel
from schemas.database import DatabaseSchema

# Desc: Create a class DatabaseService to manage the database.
class DatabaseService:
    def __init__(self, db) -> None:
        self.db = db

    # Desc: function to get all the records from the database.
    def get_all_records(self):
        return self.db.query(DatabaseModel).all()
    
    # Desc: function to create a new record in the database.
    def create_record(self, database_schema: DatabaseSchema):
            new_record = DatabaseModel(**database_schema.model_dump())
            self.db.add(new_record)
            self.db.commit()
            return None