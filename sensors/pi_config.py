import yaml

class PiConfig(object):
    def __init__(self):
        try:
            with open("./config.yaml", 'r') as stream:
                try:
                    self.config = yaml.safe_load(stream)
                    return
                except yaml.YAMLError as exc:
                    print(exc)
        except FileNotFoundError as exc:
            print(exc)
        self.config = {}

    def get_sensors(self):
        print(self.config.get('sensors', []))
        return self.config.get('sensors', [])
