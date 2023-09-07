# Desc: Import the FastAPI libraries and modules for the app.
from fastapi import FastAPI
from app.routers import users_router
from middlewares.autentification import login_router

# Desc: Import the necessary libraries and modules to response the requests.
from fastapi.responses import FileResponse
from pathlib import Path 

# Desc: Create an instance of the FastAPI class.
app = FastAPI()
app.title = "My test loging user API"
app.description = "This is the test environment for teh login section of the real app"

html_home_page_path = Path(__file__).parent / 'templates' / 'home_page.html'

# Desc: Funtion to get the home page from a HTML file.
@app.get('/', tags=['Home'], summary='Home page - Página de inicio.')
async def get_home_page():
    return FileResponse(html_home_page_path)

# Desc: Include the routers in the app.
app.include_router(users_router)

# Desc: Include the routers in the app.
app.include_router(login_router)

