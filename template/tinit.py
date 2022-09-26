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
    if yn in ["Y", "y", "yes", "Yes", "YES", ""]:
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
            if i.get("extra_commands") != None:
                if type(i["extra_commands"]) == list:
                    for j in i["extra_commands"]:
                        os.system(j)
                elif type(i["extra_commands"]) == str:
                    os.system(i["extra_commands"])
                else:
                    print("extra_commands should be string or list")
            print("==================== Done ====================")
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
        print("USAGE")
        print("\ttinit [template]")
        print("OPTIONS")
        print("\t-h, --help\tprint help")
        for i in config["template"]:
            description = ""
            if i.get("description") != None:
                description = i["description"]
            print("\t--" + i["name"], "\t", description)
    elif arg1 == "--edit" or arg1 == "-e":
        arg2 = ""
        try:
            arg2 = sys.argv[2]
        except Exception as _:
            print("Usage:")
            print("\t --edit [templatename]")
            sys.exit(0)
        edit(arg2)
    elif arg1 in ["--configure", "-c"]:
        os.system("nvim " + config_path + "/template/config.toml")
    elif arg1 in ["--path", "-p"]:
        print(config["TemplatePath"])
    elif arg1 == "comp":
        for i in config["template"]:
            if not i.get("description") in [None, ""]:
                print(i["name"] + "[" + i["description"] + "]")
            else:
                print(i["name"])
    else:
        tinit(arg1)
