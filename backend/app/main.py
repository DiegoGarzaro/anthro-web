import os
import sys
import logging


from fastapi import FastAPI
from contextlib import asynccontextmanager


sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.models.table import Table
from utils.oms_table_reader import data_reader



dfs = {}


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Scraping call
    logging.info("Scraping data from OMS")
    logging.info("Data scraped successfully")

    # Data reader call
    try:
        logging.info("Reading data")
        dfs["data"] = data_reader()
        logging.info("Data read successfully")
    except Exception as error:
        logging.critical(error)
        raise ("Error reading data")

    yield
    


app = FastAPI(lifespan=lifespan)


@app.get("/data", response_model=Table)
async def get_data():
    return dfs

    # return {"data": dfs["bmi"]["boys"]["0-to-13-weeks"]["zscores"]}
