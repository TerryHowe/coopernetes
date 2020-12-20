import os
import yaml

class PiConfig(object):
    def __init__(self):
        try:
            config_file = './config.yaml'
            sample_config_file = './sample_config.yaml'
            if (not os.path.exists(config_file) and
                os.path.exists(sample_config_file)):
                config_file = sample_config_file
                print('Warning: Using {}'.format(config_file))
            with open(config_file, 'r') as stream:
                try:
                    self.config = yaml.safe_load(stream)
                    return
                except yaml.YAMLError as exc:
                    print(exc)
        except FileNotFoundError as exc:
            print(exc)
        self.config = {}

    def get_sensors(self):
        return self.config.get('sensors', [])
