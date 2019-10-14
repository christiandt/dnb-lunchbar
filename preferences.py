import json
import keyring


class Preferences:

    def __init__(self):
        self.configuration = dict()
        self.filename = "configuration.json"
        self.read_config()

    def write_config(self):
        with open(self.filename, 'wb') as f:
            f.write(json.dumps(self.configuration))

    def read_config(self):
        with open(self.filename, 'r') as f:
            self.configuration = json.loads(f.read())

    @property
    def username(self):
        return str(self.configuration['email'])

    @username.setter
    def username(self, value):
        self.configuration['email'] = str(value)

    @property
    def password(self):
        return str(keyring.get_password("pylunch", self.username))

    @password.setter
    def password(self, value):
        keyring.set_password("pylunch", self.username, str(value))

    @property
    def interval(self):
        return int(self.configuration['interval'])

    @interval.setter
    def interval(self, value):
        self.configuration['interval'] = int(value)

    @property
    def show_currency(self):
        if 'show_currency' in self.configuration:
            return bool(self.configuration['show_currency'])
        return False

    @show_currency.setter
    def show_currency(self, value):
        self.configuration['show_currency'] = bool(value)

    @property
    def config(self):
        return self.configuration

    @config.setter
    def config(self, value):
        self.configuration = value


