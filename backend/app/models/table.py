from pydantic import BaseModel
import pandas as pd

class Table(BaseModel):
    data: dict