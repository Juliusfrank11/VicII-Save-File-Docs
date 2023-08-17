import json
import re
import copy
import os
from pydantic import ValidationError


def fix_religion_culture(POP_dict):
    religions = "catholic coptic orthodox protestant gelugpa hindu mahayana shinto sikh theravada jewish shiite sunni animist".split()
    new_dict = {}
    for k, v in POP_dict.items():
        if v in religions:
            new_dict["culture"] = {"name": k, "religion": v}
        else:
            new_dict[k] = v
    return new_dict


def collect_repeated_keys(dictionary):
    def is_all_digits(string):
        return all([c in "0123456789." for c in string])

    original = copy.deepcopy(dictionary)
    searched_keys = list(dictionary.keys())
    confirmed_duplicate_keys = []
    for key, value in original.items():
        # if the value is a nested dictionary, recursively collect its keys
        if key not in confirmed_duplicate_keys:
            if isinstance(value, dict):
                dictionary[key] = collect_repeated_keys(value)
            # if the value is a list of dictionaries, recursively collect keys for each dictionary in the list
            elif isinstance(value, list) and all(
                isinstance(item, dict) for item in value
            ):
                dictionary[key] = [collect_repeated_keys(item) for item in value]
            # if the key is repeated, collect the repeated keys into a single key
            # WHY THE FUCK IS THERE A KEY CALLED `money2` AND IT'S A BOOLEAN!?!??!
            if f"{key}2" in searched_keys and not is_all_digits(key) and key != "money":
                collection = [
                    {"this_is_a_repeated_key_please_collapse_down": True},
                    value,
                ]
                repeated_keys = []
                i = 2
                exhausted_keys = False
                while not exhausted_keys:
                    try:
                        key_to_find = f"{key}{i}"
                        collection.append(dictionary[key_to_find])
                        repeated_keys.append(key_to_find)
                        i += 1
                    except KeyError:
                        exhausted_keys = True
                dictionary[key] = collection
                for k in repeated_keys:
                    del dictionary[k]
                    searched_keys.remove(k)
                    confirmed_duplicate_keys.append(k)

    return dictionary


def dict_depth(my_dict):
    if isinstance(my_dict, dict):
        return 1 + (max(map(dict_depth, my_dict.values())) if my_dict else 0)
    return 0


if not os.path.exists("consolidated_json_save.json"):
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
    consolidated_json_save = collect_repeated_keys(json_save)
    for _ in range(dict_depth(consolidated_json_save)):
        # extremely dumb and slow, but it works
        consolidated_json_save = collect_repeated_keys(consolidated_json_save)
    # fix Pop culture label
    # it's usually {culture}={religion} like french=catholic, which is dumb
    # changes to {culture: {name: `{culture}`, religion: `{religion}` }}
    for k, v in consolidated_json_save["province_data"].items():
        pop_types = "craftsmen farmers labourers slaves soldiers artisans bureaucrats clergymen clerks officers aristocrats capitalists".split()
        religions = "catholic coptic orthodox protestant gelugpa hindu mahayana shinto sikh theravada jewish shiite sunni animist".split()
        for pop_type in pop_types:
            pops = v.get(pop_type)
            if pops is not None:
                if isinstance(pops, dict):
                    consolidated_json_save["province_data"][k][
                        pop_type
                    ] = fix_religion_culture(pops)
                elif isinstance(pops, list):
                    consolidated_json_save["province_data"][k][pop_type] = [
                        fix_religion_culture(pop) for pop in pops
                    ]
    json.dump(consolidated_json_save, open("consolidated_json_save.json", "w"))
else:
    with open("consolidated_json_save.json", "r") as f:
        json_save = json.load(f)

from models import VicIISave

try:
    VicIISave(**json_save)
except ValidationError as e:
    print(e)
    """
    error_string_lines = str(e).splitlines()
    # just ignoring dict and list errors for repeated keys until the end
    for n, line in enumerate(error_string_lines):
        if "is not a valid list" in line or "is not a valid dict" in line:
            pass
        else:
            try:
                if (
                    "is not a valid list" in error_string_lines[n + 1]
                    or "is not a valid dict" in error_string_lines[n + 1]
                ):
                    pass
                else:
                    print(line)
            except IndexError:
                print(line)
    """
