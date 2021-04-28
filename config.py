import yaml

class Config():

    def __init__(self):
        with open("config.yaml") as config_file:
            self.config = yaml.safe_load(config_file)

    def __getattr__(self, name):
        try:
            return self.config[name]
        except KeyError:
            return getattr(self.args, name)

config = Config()