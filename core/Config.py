import json
from enum import Enum


class ConfigType(Enum):
    INT = 1
    BOOL = 2
    STR = 3
    USER = 4
    CHANNEL = 5


class Config(dict):
    def __init__(self, config_db, name, config_type=ConfigType.STR, default=None, required=False, description=None,
                 module=None):
        super().__init__()
        self.config_db = config_db
        self.name = name
        self.config_type = config_type
        self.default = default
        self.required = required
        self.description = description
        self.module = module

    def __iter__(self):
        pass

    def __len__(self):
        pass

    def __delitem__(self, key):
        self.config_db.reset(self.name, key, self.module)

    def __getitem__(self, item):
        try:
            return self.config_db.get(self.name, item, self.module)
        except KeyError:
            return self.default

    def __setitem__(self, key, value):
        self.config_db.set(self.name, key, value, self.module)


class ConfigDatabase:
    _database = {}
    _configs = {}

    def loads(self, guild_id):
        try:
            with open(f'./config/{guild_id}.json', 'r') as f:
                self._database[guild_id] = json.load(f)
        except FileNotFoundError:
            self._database[guild_id] = {}

    def reset(self, name, guild_id, module=None):
        try:
            if module:
                del self._database[guild_id][module][name]
            else:
                del self._database[guild_id][name]
        except KeyError:
            pass

    def get(self, name, guild_id, module=None):
        if module:
            return self._database[guild_id][module][name]
        else:
            return self._database[guild_id][name]

    def set(self, name, guild_id, value, module=None):
        try:
            if module:
                self._database.setdefault(guild_id, {}).setdefault(module, {})[name] = value
            else:
                self._database.setdefault(guild_id, {})[name] = value
            with open(f'config/{guild_id}.json', 'w') as f:
                json.dump(self._database[guild_id], f)
        except KeyError:
            pass

    def add(self, name, config_type=ConfigType.STR, default=None, required=False,
            description=None, module=None):
        config = Config(self, name, config_type, default, required, description, module)

        if module:
            self._configs.setdefault(module, {})[name] = config
        else:
            self._configs[name] = config

        return config
