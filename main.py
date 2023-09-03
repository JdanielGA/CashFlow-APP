# Desc: Import the necessary libraries to launch the application.
from fastapi import FastAPI

# Desc: Import the necessary modules to response.
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
@app.get('/home', tags=['Home'])
async def get_home_page():
    return FileResponse(html_home_page_path)
