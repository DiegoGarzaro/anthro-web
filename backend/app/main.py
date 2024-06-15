import os
import sys



from fastapi import FastAPI
from contextlib import asynccontextmanager


sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils.oms_table_reader import data_reader
from utils.logger import Logger

logger = Logger()


dfs = {}


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Scraping call
    logger.info("Scraping data from OMS")
    logger.info("Data scraped successfully")

    # Data reader call
    try:
        logger.info("Reading data")
        dfs["data"] = data_reader()
        logger.info("Data read successfully")
    except Exception as error:
        logger.critical(error)
        raise ("Error reading data")

    yield
    


app = FastAPI(lifespan=lifespan)


@app.get("/data", tags=["Data"], description="Get the data")
async def get_data():
    return dfs

    # return {"data": dfs["bmi"]["boys"]["0-to-13-weeks"]["zscores"]}
