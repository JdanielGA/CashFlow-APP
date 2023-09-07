from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.responses import JSONResponse
import csv


# Desc: Create the class to manage the users.
class User:
    def __init__(self, id: str, first_name: str, last_name: str, email: str, password: str):
        self.data = {}
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self._password = generate_password_hash(password)
        self.data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self._password
        }
    
    # Desc: Function to set the password.
    def set_password(self, password):
        self._password = generate_password_hash(password)
    
    # Desc: Function to check the password.
    def check_password(self, password):
        return check_password_hash(self._password, password)

    # Desc: Function to get the data from the user.
    def get_data(self):
        return self.data


# Desc: Create a class to manage the database from a csv file and calling the User class.
class UsersDB:
    def __init__(self):
        self.__databae_path = './database/database.csv'
        self.users_database = []
        self.user_data = {}

    # Desc: Function to get the data from the csv file.
    def get_recors(self):
        headers = ['id', 'first_name', 'last_name', 'email', 'password']
        # Desc: Verify if the file has 
        try:
            with open(self.__databae_path, 'r', encoding='utf-8', newline='') as file:
                reader = csv.DictReader(file)
                self.users_database = list(reader)
                return self.users_database
        
        except FileNotFoundError:
            with open(self.__databae_path, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                return None
        
    # Desc: Function to get a user by id from the database.
    def get_user_by_id(self, id):
        self.users_database = self.get_recors()
        for user in self.users_database:
            if user['id'] == id:
                return user
        return None
    
    # Desc: Function to get a user by email from the database.
    def get_user_by_email(self, email):
        self.users_database = self.get_recors()
        for user in self.users_database:
            if user['email'] == email:
                return user
        return None


    # Desc: Function to create a new user calling the User class.
    def create_user(self, id, first_name, last_name, email, password):
        new_user = User(id, first_name, last_name, email, password)
        self.user_data = new_user.get_data()
        with open(self.__databae_path, 'a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.user_data.keys())
            writer.writerow(self.user_data)
        return {'message': 'The user was created successfully.'}
    
    # Desc: Function to login a user.
    def login(self, email, password):
        user = self.get_user_by_email(email)
        if user is not None:
            check_password = check_password_hash(user['password'], password)
            if check_password:
                # Desc: Return the user Full Name.
                return user['first_name'] + ' ' + user['last_name']
            else:
                return False
        return None
        