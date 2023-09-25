# Used to replace the PDX format with python-like tabbed format

# TODO: find way to group history in the war structure

import os
import json
import copy
import re


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
            if f"{key}(2)" in searched_keys:
                collection = {"this_is_a_repeated_key_please_collapse_down": []}

                repeated_keys = []
                i = 2
                exhausted_keys = False
                while not exhausted_keys:
                    try:
                        key_to_find = f"{key}({i})"
                        collection[
                            "this_is_a_repeated_key_please_collapse_down"
                        ].append(dictionary[key_to_find])
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


def make_tabbed_saves():
    if not os.path.exists("tabbed_saves/"):
        os.mkdir("tabbed_saves")

    for save_filename in os.listdir("saves"):
        with open(
            f"saves/{save_filename}", "r", encoding="windows-1252", errors="ignore"
        ) as save:
            lines = [L.strip() for L in save.readlines()]

        with open(
            f"tabbed_saves/{save_filename}",
            "w",
            encoding="windows-1252",
            errors="ignore",
        ) as tabbed_save:
            level = 0
            for n, line in enumerate(lines):
                tabbed_save.write("".join(["\t" for i in range(level)]))
                for c in line:
                    if c == "{":
                        level += 1
                        tabbed_save.write("\n" + "".join(["\t" for i in range(level)]))
                    elif c == "}":
                        level -= 1
                        tabbed_save.write("\n" + "".join(["\t" for i in range(level)]))
                    else:
                        tabbed_save.write(c)
                tabbed_save.write("\n")
        print(f"Converted {save_filename} to tabbed save")


def make_json_saves():
    if not os.path.exists("json_saves/"):
        os.mkdir("json_saves")

    for save_filename in os.listdir("tabbed_saves"):
        with open(
            f"tabbed_saves/{save_filename}",
            "r",
            encoding="windows-1252",
            errors="ignore",
        ) as save:
            lines = [L.replace("\n", "") for L in save.readlines()]

        save_dict = {}
        max_level = max([L.count("\t") for L in lines]) - 1

        key_list = [None for _ in range(max_level)]

        current_level = 0
        previous_level = 0
        for n, line in enumerate(lines):
            current_level = line.count("\t")
            if current_level < previous_level:
                for i in range(previous_level, max_level):
                    key_list[i] = None
            if "=" in line:
                try:
                    key, value = line.split("=")
                    # to handle french names with a '
                    value = value.replace("'", "\\'")
                    value = value.strip()
                    key_list[current_level] = key.strip()
                    key_string = "".join(
                        [f"['{k}']" for k in key_list if k is not None]
                    )
                    if value:
                        code = f"save_dict{key_string} = '{value}'"
                    else:
                        # don't add duplicate keys
                        try:
                            i = 1
                            while True:
                                if i < 2:
                                    exec(f"leaf= save_dict{key_string}")
                                    i += 1
                                else:
                                    key_list[current_level] = f"{key.strip()}({i})"
                                    key_string = "".join(
                                        [f"['{k}']" for k in key_list if k is not None]
                                    )
                                    exec(f"leaf= save_dict{key_string}")
                                    i += 1
                        except KeyError:
                            # scan for array
                            j = 1
                            array_found = False
                            while "=" not in lines[n + j]:
                                if lines[n + j].split():
                                    if all(
                                        [
                                            c in "0123456789.- "
                                            for c in lines[n + j].strip()
                                        ]
                                    ) or all(
                                        [
                                            w[-1] == '"' and w[0] == '"'
                                            for w in lines[(n + j)].split()
                                        ]
                                        # TODO: handle strings with spaces
                                    ):
                                        array = lines[n + j].strip().split()
                                        code = f"save_dict{key_string} = {array}"
                                        array_found = True
                                        break
                                j += 1
                            if not array_found:
                                code = f"save_dict{key_string} = " + "{}"

                    exec(code)
                except ValueError:
                    print(f"ValueError: {line}")
            previous_level = current_level
        with open(
            f"json_saves/{save_filename.replace('.v2','.json')}", "w"
        ) as json_save:
            json.dump(save_dict, json_save)
        print(f"Converted {save_filename} to json save")


def make_consolidated_json_saves():
    if not os.path.exists("consolidated_json_saves/"):
        os.mkdir("consolidated_json_saves")
    for save_file in os.listdir("json_saves/"):
        with open(f"json_saves/{save_file}", "r", errors="ignore") as f:
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
            for pop_type in pop_types:
                pops = v.get(pop_type)
                if pops is not None:
                    if "this_is_a_repeated_key_please_collapse_down" not in pops.keys():
                        consolidated_json_save["province_data"][k][
                            pop_type
                        ] = fix_religion_culture(pops)
                    else:
                        consolidated_json_save["province_data"][k][pop_type][
                            "this_is_a_repeated_key_please_collapse_down"
                        ] = [
                            fix_religion_culture(pop)
                            for pop in pops[
                                "this_is_a_repeated_key_please_collapse_down"
                            ]
                        ]
        json.dump(
            consolidated_json_save, open(f"consolidated_json_saves/{save_file}", "w")
        )
        print(f"Converted {save_file} to consolidated json")


def main():
    make_tabbed_saves()
    make_json_saves()
    make_consolidated_json_saves()


if __name__ == "__main__":
    main()
