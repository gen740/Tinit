import os
import sys
import shutil
from typing import Any, Dict
import toml

config: Dict[str, Any]


def tinit(name: str):
    global config
    for i in config["template"]:
        if i["name"] == name:
            # shutil.copy("")
            os.path.join(config["TemplatePath"])
            print(config["Path"])


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
            try:
                description = i["description"]
            except Exception as e:
                raise e
            print("\t--", i["name"], "\t", description)
        sys.exit(0)
    else:
        tinit(arg1)
    print("Tinit Done")
