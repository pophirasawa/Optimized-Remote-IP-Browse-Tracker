import yaml
import os


example_config = yaml.load(
    """
    authorization: 'yourauthorizationkey'
    encodingkey: 'yourencodingkey'
    serveraddress: 'https://127.0.0.1'
    """,
    Loader=yaml.Loader,
)


class ConfigLoader:
    _instance = None
    _init = False
    default_config = example_config

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

    def generate_config(self):
        config = self.default_config
        tmp_doc = yaml.dump(config)
        return tmp_doc

    def check_config(self, config):
        if not set(self.default_config.keys()).issubset(set(config.keys())):
            return False

        # 检查嵌套字典
        for key in self.default_config.keys():
            if isinstance(self.default_config[key], dict):
                if not isinstance(config[key], dict):
                    return False

                if not set(self.default_config[key].keys()).issubset(
                    set(config[key].keys())
                ):
                    return False

        return True

    def load_yaml(self):
        path_exist = os.path.exists(self.config_path)

        if not path_exist:
            with open(self.config_path, "w+", encoding="utf-8") as f:
                new_config = self.generate_config()
                f.write(new_config)
                config = yaml.load(new_config, Loader=yaml.Loader)

        else:
            with open(self.config_path, "r+", encoding="utf-8") as f:
                loaded = yaml.load(f, Loader=yaml.Loader)

                is_loaded_legal = self.check_config(loaded)

                if is_loaded_legal:
                    config = loaded

                else:
                    raise Exception("配置文件异常, 请检查yaml文件")

        return config
