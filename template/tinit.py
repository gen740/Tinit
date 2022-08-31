import os
import sys
import shutil
from typing import Any, Dict
import toml

config: Dict[str, Any]


def edit(name: str):
    """
    edit the template files
    """
    global config
    files = ""
    for i in config["template"]:
        if i["name"] == name:
            for j in i["files"]:
                files += os.path.join(config["TemplatePath"], j) + " "
            break
    else:
        print("There in no match template: ", name)
        sys.exit(1)
    # Confirm Prompt
    print("will edit ", files)
    yn = input("Y/n: ")
    if yn in ["Y", "y", "yes", "Yes", "YES"]:
        os.system("nvim " + files)
    else:
        sys.exit(0)


def tinit(name: str):
    global config
    for i in config["template"]:
        i: Dict[str, Any]
        if i["name"] == name:
            if i.get("to") != None:
                for j, k in zip(i["files"], i["to"]):
                    shutil.copy(os.path.join(config["TemplatePath"], j), k)
            else:
                for j in i["files"]:
                    shutil.copy(os.path.join(config["TemplatePath"], j), ".")
            break
    else:
        print("There in no match template: ", name)
        sys.exit(1)


def run():
    global config
    config_path = ""
    try:
        config_path = os.environ["XDG_CONFIG_HOME"]
    except Exception as _:
        print("Plese Set XDG_CONFIG_HOME")
        sys.exit(1)
    config = toml.load(config_path + "/template/config.toml")
    arg1 = ""
    if len(sys.argv) > 1:
        arg1 = sys.argv[1]
    if arg1 == "--help" or arg1 == "-h" or arg1 == "":
        print("Command:")
        for i in config["template"]:
            description = ""
            if i.get("description") != None:
                description = i["description"]
            print("\t--", i["name"], "\t", description)
        sys.exit(0)
    if arg1 == "--edit" or arg1 == "-e":
        arg2 = ""
        try:
            arg2 = sys.argv[2]
        except Exception as _:
            print("Usage:")
            print("\t --edit [templatename]")
            sys.exit(0)
        edit(arg2)

    else:
        tinit(arg1)
    print("==================== Tinit Done ====================")
