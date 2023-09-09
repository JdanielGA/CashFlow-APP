# Desc: Import the main libraries and modules.
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

# Desc: Import components from my own modules.
from config.database import Base, engine
from routers.users import users_router
from routers.login import login_router
from routers.database import database_router

# Desc: Instance of the FastAPI class.
app = FastAPI()
app.title = "FastAPI Demo"
app.description = "This is a simple demo of FastAPI."
app.version = "1.0.0"


# Desc: Path to the home page
html_home_page_path = Path(__file__).parent / 'template' / 'index.html'

# Desc: Home page using the FileResponse class and the html_home_page_path variable.
@app.get('/', tags=['Home'], summary='Home page - Página de inicio.')
async def get_home_page():
    return FileResponse(html_home_page_path)

# Desc: Create the database tables.
Base.metadata.create_all(bind=engine)

# Desc: Import the database routers.
app.include_router(database_router)

# Desc: Import the user routers.
app.include_router(users_router)

# Desc: Import the login router.
app.include_router(login_router, include_in_schema=False)

