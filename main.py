from fastapi import FastAPI, Body
from models import VicIISave
from typing import Annotated

app = FastAPI()


@app.post("/save")
def create_v2_save(save: Annotated[VicIISave, Body()]):
    return save
