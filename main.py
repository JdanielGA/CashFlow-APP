# Desc: Import the necessary libraries and modules to launch the application.
from fastapi import FastAPI, Query
from middlewares import error_handler, autentification
from config.database import engine, Base_database
from routers.database import database_router
from routers.users import users_router
from routers.login import login_router

# Desc: Import the necessary libraries and modules to response the requests.
from fastapi.responses import FileResponse
from pathlib import Path 

# Desc: Create an instance of the FastAPI class.
app = FastAPI()
app.title = 'CashFlow APP'
app.description = 'CashFlow APP is a application that allows manage the cash flow of a company.'
app.version = '0.0.1'

# Desc: Create a path to the home page.
html_home_page_path = Path(__file__).parent / 'templates' / 'home_page.html'

# Desc: Funtion to get the home page from a HTML file.
@app.get('/', tags=['Home'], summary='Home page - Página de inicio.')
async def get_home_page():
    return FileResponse(html_home_page_path)

# Desc: Add the error handler middleware to the application.
app.add_middleware(error_handler.ErrorHandler)

# Desc: Create the database tables.
Base_database.metadata.create_all(bind=engine)

# Desc: Add the login router to the application.
app.include_router(login_router)

# Desc: Add the database router to the application.
app.include_router(database_router)

# Desc: Add the users router to the application.
app.include_router(users_router)