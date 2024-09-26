import yaml
import os
import uuid

example_doc = """
server:
 address: 'yourSeverAddress'
 authorization: 'yourauthorizationkey'
updatefreq: 30
encodingkey: 'yourencodingkey'
name: 'hostname'
"""


class ConfigLoader:
    _instance = None
    _init = False

    def __init__(self, path=None):
        if self._init and path:
            return

        DEFAULT_CONFIG_PATH = "A.yaml"
        self._init = True

        if path:
            self.config_path = path

        if not hasattr(self, "config_path"):
            self.config_path = DEFAULT_CONFIG_PATH

        self.config = self.load_yaml()

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(ConfigLoader, cls).__new__(cls)

        return cls._instance

    def load_yaml(self):
        path_exist = os.path.exists(self.config_path)

        if not path_exist:
            my_uid = uuid.uuid4()
            config = yaml.load(example_doc, Loader=yaml.Loader)
            config["server"].update({"uid": str(my_uid)})
            tmp_doc = yaml.dump(config)
            with open(self.config_path, "w+", encoding="utf-8") as f:
                f.write(tmp_doc)

        else:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = yaml.load(f, Loader=yaml.Loader)

        return config
