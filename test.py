from validators import validate_tag
import json
import re
import copy

with open("json_saves/autosave.json", "r") as f:
    raw_json_save = json.load(f)

json_save = copy.deepcopy(raw_json_save)

# collect nation data and province in "nation_data" key
json_save["nation_data"] = {}
json_save["province_data"] = {}
for k, v in raw_json_save.items():
    if re.match(r"\b([A-Z]{3}|D[0-9]{2})\b", k):
        json_save["nation_data"][k] = v
        del json_save[k]
    elif re.match(r"[0-9]{1,4}", k):
        json_save["province_data"][k] = v
        del json_save[k]


def collect_repeated_keys(d, base_key=None, counter=1):
    # base case: no keys left in the dictionary
    if len(d) == 0:
        return {}

    # if base_key is not provided, find the base key
    if base_key is None:
        base_key = sorted(d.keys())[0]
        base_value = d.pop(base_key)
    else:
        base_value = []

    # find related keys
    related_keys = [key for key in d.keys() if key.startswith(base_key)]

    # collect values of the related keys and remove them from the dictionary
    for key in related_keys:
        base_value.append(d[key])
        del d[key]

    # assign the list of values to the base key
    d[base_key] = base_value

    # call the function recursively to process the remaining keys in the dictionary
    collect_repeated_keys(d)

    return d


json_save = collect_repeated_keys(json_save)

from models import VicIISave

VicIISave(**json_save)
