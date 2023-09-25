import json
from pydantic import ValidationError
import os

save = ""

for file in os.listdir("consolidated_json_saves/"):
    print(file)
    if save:
        with open(save, "r") as f:
            json_save = json.load(f)
    else:
        with open(f"consolidated_json_saves/{file}", "r") as f:
            json_save = json.load(f)

    from models import VicIISave

    try:
        VicIISave(**json_save)
    except ValidationError as e:
        print(e)  # redirects to stout
    if save:
        break
