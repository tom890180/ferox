import yaml


class Config:
    def __init__(self):
        self.cfg = {}

        with open("conf.yml", 'r') as stream:
            try:
                self.cfg = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def get(self):
        return self.cfg
