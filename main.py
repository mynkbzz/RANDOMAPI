from fastapi import FastAPI, Request
import random
import jinja2
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import asyncpg
import sqlalchemy
import databases


# DATABASE_URL = "postgresql://postgres:root@localhost/testdb"

# database = databases.Database(DATABASE_URL)


app = FastAPI()


@app.on_event("startup")
async def start():
    global conn
    conn = await asyncpg.connect("postgresql://postgres:root@localhost/testdb")


# @app.on_event("startup")
# def startup():
#     database.connect()


# @app.on_event("shutdown")
# def shutdown():
#     database.disconnect()

# Was trying with list now no need
# listofvideos = []
# listofvideos.append("https://www.youtube.com/watch?v=xna_PkWzPVE")
# listofvideos.append("https://www.youtube.com/watch?v=jzbMxWvnlGw")
# listofvideos.append("https://www.youtube.com/watch?v=vJVqUwc9J7g")

templates = Jinja2Templates(directory="templates")


async def getlink():
    sql = f"Select link FROM randomlinks ORDER BY RANDOM() LIMIT 1"
    links_is = await conn.fetch(sql)
    return links_is


@app.get("/front/", response_class=HTMLResponse)
async def read_item(request: Request):
    linklelo = await getlink()
    context = {"request": request, "linklelo": linklelo}
    return templates.TemplateResponse("front.html", context)
