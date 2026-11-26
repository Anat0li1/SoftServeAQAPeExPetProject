import configparser


class ConfigLoader:
    def __init__(self, file_path):
        parser = configparser.ConfigParser()
        parser.read(file_path, encoding="utf-8")

        for key, value in parser.defaults().items():
            setattr(self, key.upper(), self.convert_value(value))

    def convert_value(self, value):
        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            pass

        return value
