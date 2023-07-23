# Used to replace the PDX format with python-like tabbed format

import os
import json


def make_tabbed_saves():
    if not os.path.exists("tabbed_saves/"):
        os.mkdir("tabbed_saves")

    for save_filename in os.listdir("saves"):
        with open(
            f"saves/{save_filename}", "r", encoding="windows-1252", errors="ignore"
        ) as save:
            lines = [l.strip() for l in save.readlines()]

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
            lines = [l.replace("\n", "") for l in save.readlines()]

        save_dict = {}
        max_level = max([l.count("\t") for l in lines]) - 1

        key_list = [None for i in range(max_level)]

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
                                    key_list[current_level] = key.strip() + str(i)
                                    key_string = "".join(
                                        [f"['{k}']" for k in key_list if k is not None]
                                    )
                                    exec(f"leaf= save_dict{key_string}")
                                    i += 1
                        except KeyError:
                            # scan for array
                            # TODO: add support for non-numeric arrays
                            j = 1
                            array_found = False
                            while "=" not in lines[n + j]:
                                if lines[n + j].split():
                                    if all(
                                        [
                                            c in "0123456789.- "
                                            for c in lines[n + j].strip()
                                        ]
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


def main():
    make_tabbed_saves()
    make_json_saves()


if __name__ == "__main__":
    main()
