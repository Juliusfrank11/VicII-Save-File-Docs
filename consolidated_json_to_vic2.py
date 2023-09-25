import os
import json

repeated_key_indicator = "this_is_a_repeated_key_please_collapse_down"

if not os.path.exists("created_saves"):
    os.mkdir("created_saves")

consolidated_json_save_path = "consolidated_json_saves/Netherlands1919_05_08.json"
with open(consolidated_json_save_path, "r") as f:
    save = json.load(f)

# collapse down nation_data and province_data
for k, v in save["nation_data"].items():
    save[k] = v
del save["nation_data"]
for k, v in save["province_data"].items():
    save[k] = v
del save["province_data"]


def list_to_pdx_array(li):
    if not isinstance(li, list):
        return li
    else:
        return "{" + " ".join(li) + "}"


def dict_to_vic2(d):
    pdx_format = ""

    if isinstance(d, dict):
        for k, v in d.items():
            print(k, v)
            if k == "news_collector":
                pdx_format += "news_collector = {}"
                continue
            if k == "culture" and isinstance(v, dict):
                pdx_format += f"{v['name']} = {v['religion']}"
            else:
                if not isinstance(v, dict):
                    if isinstance(v, list):
                        if k != repeated_key_indicator:
                            pdx_format += f"{k} = " + "{" + " ".join(v) + "}"
                        else:
                            for repeated_key in v:
                                pdx_format += (
                                    f"{k} = " "{" + dict_to_vic2(repeated_key) + "}\n"
                                )
                    else:
                        pdx_format += f"{k} = {v}"
                else:
                    if list(v.keys()) == [repeated_key_indicator]:
                        for repeated_key in v[repeated_key_indicator]:
                            if isinstance(repeated_key, list):
                                pdx_format += (
                                    f"{k} = "
                                    "{"
                                    + " ".join(
                                        [
                                            list_to_pdx_array(i)
                                            for i in v[repeated_key_indicator]
                                        ]
                                    )
                                    + "}\n"
                                )
                            else:
                                pdx_format += (
                                    f"{k} = " "{" + dict_to_vic2(repeated_key) + "}\n"
                                )
                    else:
                        pdx_format += f"{k} = " + "{" + dict_to_vic2(v) + "}\n"
            pdx_format += "\n"
    elif isinstance(d, list):
        pdx_format += "{\n"
        for i in d:
            pdx_format += "{" + " ".join(i) + "}"
    return pdx_format


with open("created_saves/test.v2", "w") as f:
    f.write(dict_to_vic2(save))
