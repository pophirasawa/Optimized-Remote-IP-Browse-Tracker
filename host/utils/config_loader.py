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
class ConfigLoader():
    _instance = None
    _init = False
    def __init__(self, path = None):
        DEFAULT_CONFIG_PATH = 'A.yaml'
        if self._init is True and path is None:
            return
        self._init = True
        if path is not None:
            self.config_path = path
        if hasattr(self, "config_path") is False:
            self.config_path = DEFAULT_CONFIG_PATH
        self.config = self.load_yaml()
  

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
        return cls._instance

    def load_yaml(self):
        if os.path.exists(self.config_path) == False:
            my_uid = uuid.uuid4()
            config = yaml.load(example_doc, Loader=yaml.Loader)
            config['server'].update({'uid': str(my_uid) })
            tmp_doc = yaml.dump(config)
            with open(self.config_path,'w+') as f:
                f.write(tmp_doc)
        else:
            with open(self.config_path, 'r') as f:
                config = yaml.load(f, Loader=yaml.Loader)
        return config

