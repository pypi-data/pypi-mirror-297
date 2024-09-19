import json
from os.path import isfile, join, expanduser

from xdg import BaseDirectory as XDG

from chatterbox_bus_client.client import MessageBusClient


def get_bus_config(base_folder="chatterbox"):
    # look for the default bus.conf
    # NOTE: this is uncommon and not really used in the wild,
    # regardless it is in the SPEC
    for path in XDG.load_config_paths(base_folder):
        config = join(path, "bus.conf")
        if isfile(config):
            with open(config) as f:
                conf = json.load(f)
                return conf

    file_path = f"/etc/{base_folder}/bus.conf"
    if isfile(file_path):
        with open(file_path) as f:
            conf = json.load(f)
            return conf

    file_path = expanduser(f"~/.{base_folder}/bus.conf")
    if isfile(file_path):
        with open(file_path) as f:
            conf = json.load(f)
            return conf

    # try to import the config from the chatterbox module, might not be
    # installed!
    try:
        from chatterbox.configuration import Configuration
        conf = Configuration.get().get("websocket", {})
    except ImportError:
        conf = {}

    # manually check known .conf paths
    # check default chatterbox user config, then check for a dedicated user
    # named chatterbox, then xdg paths, and finally the system config
    paths = [expanduser(f"~/.{base_folder}/{base_folder}.conf"),
             f"/home/{base_folder}/.{base_folder}/{base_folder}.conf"] +\
            [join(p, f"{base_folder}.conf")
             for p in XDG.load_config_paths(base_folder)] + \
            [f"/etc/{base_folder}/{base_folder}.conf"]

    for file_path in paths:
        if conf:
            break
        if isfile(file_path):
            with open(file_path) as f:
                commented_json = f.read().split("\n")
                for idx, line in enumerate(commented_json):
                    if line.strip().startswith("//"):
                        commented_json[idx] = ""
                clean_json = "\n".join(commented_json)
                if clean_json: # can be empty file
                    conf = json.loads("\n".join(commented_json))
                    conf = conf.get("websocket", {})

    # fallback to mycroft.conf to account for HolmesV based projects
    if not conf:
        try:
            from mycroft.configuration import Configuration
            conf = Configuration.get().get("websocket", {})
        except ImportError:
            pass

    # extreme fallback, check all paths above for mycroft instead of chatterbox
    if not conf and base_folder == "chatterbox":
        return get_bus_config("mycroft")
    return conf


def client_from_config(subconf='core', file_path='/etc/chatterbox/bus.conf'):
    """Load messagebus configuration from file.

    The config is a basic json file with a number of "sub configurations"

    Ex:
    {
      "core": {
        "route": "/core",
        "port": "8181"
      }
    }

    if .conf not found and subconf='core'
        - look for chatterbox.conf in standard locations
        - look for mycroft.conf in standard locations

    Arguments:
        subconf:    configuration to choose from the file, defaults to "core"
                    if omitted.
        file_path:  path to the config file, defaults to /etc/chatterbox/bus.conf
                    if omitted.
    Returns:
        MessageBusClient instance based on the selected config.
    """
    if isfile(file_path):
        with open(file_path) as f:
            conf = json.load(f)
    else:
        conf = get_bus_config()

    if subconf in conf:
        conf = conf[subconf]

    return MessageBusClient(host=conf.get("host", "0.0.0.0"),
                            port=conf.get("port", 8181),
                            route=conf.get("route", "/core"),
                            ssl=conf.get("ssl", False))
