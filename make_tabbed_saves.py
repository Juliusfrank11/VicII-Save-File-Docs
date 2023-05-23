# Used to replace the PDX format with python-like tabbed format

import os

def make_tabbed_saves():
    if not os.path.exists("tabbed_saves/"):
        os.mkdir("tabbed_saves")
    
    for save_filename in os.listdir("saves"):
        # I'm sure ignoring utf errors will not do anything bad
        # ^ clueless
        with open(f"saves/{save_filename}","r",errors="ignore") as save:
            lines = [l.strip() for l in save.readlines()]

        with open(f"tabbed_saves/{save_filename}","w") as tabbed_save:
            level = 0
            for line in lines:
                tabbed_save.write("".join(["\t" for i in range(level)]))
                for c in line:
                    if c == "{":
                        level += 1
                    elif c == "}":
                        level -= 1
                    else:
                        tabbed_save.write(c)
                tabbed_save.write("\n")

def main():
    make_tabbed_saves()

if __name__ == "__main__":
    main()