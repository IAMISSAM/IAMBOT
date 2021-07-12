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
        try:
            self.config_db.reset(self.name, key, self.module)
        except KeyError:
            pass

    def __getitem__(self, item):
        try:
            return self.config_db.get(self.name, item, self.module)
        except KeyError:
            return self.default

    def __setitem__(self, key, value):
        try:
            self.config_db.set(self.name, key, value, self.module)
        except KeyError:
            pass


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
        if module:
            del self._database[guild_id][module][name]
        else:
            del self._database[guild_id][name]
        with open(f'config/{guild_id}.json', 'w') as f:
            json.dump(self._database[guild_id], f)

    def get(self, name, guild_id, module=None):
        if module:
            return self._database[guild_id][module][name]
        else:
            return self._database[guild_id][name]

    def get_or(self, name, guild_id, default, module=None):
        try:
            return self.get(name, guild_id, module)
        except KeyError:
            return default

    def set(self, name, guild_id, value, module=None):
        if module:
            self._database.setdefault(guild_id, {}).setdefault(module, {})[name] = value
        else:
            self._database.setdefault(guild_id, {})[name] = value
        with open(f'config/{guild_id}.json', 'w') as f:
            json.dump(self._database[guild_id], f)

    def add(self, name, config_type=ConfigType.STR, default=None, required=False,
            description=None, module=None):
        config = Config(self, name, config_type, default, required or default is None, description, module)

        if module:
            self._configs.setdefault(module, {})[name] = config
        else:
            self._configs[name] = config

        return config

    def has_missing_required_config(self, guild_id, module_name):
        if module_name not in self._configs:
            return False

        for config_name in self._configs[module_name]:
            config = self._configs[module_name][config_name]
            if config[guild_id] is None and config.default is None and config.required:
                return True

        return False

    def get_module_configs(self, module):
        if module not in self._configs:
            return {}
        else:
            return self._configs[module]


def config_to_string(config: Config, ctx):
    description = ""
    description += f'\n:gear: **__{config.name}{"*" if config.required else ""}__**:\n'
    if config.description:
        description += f':ledger: {config.description}\n'
    value_emoji = ":1234:"
    if config.config_type == ConfigType.BOOL:
        value_emoji = ":question:"
    elif config.config_type == ConfigType.STR:
        value_emoji = ":abc:"
    elif config.config_type == ConfigType.USER:
        value_emoji = ":bust_in_silhouette:"
    elif config.config_type == ConfigType.CHANNEL:
        value_emoji = ":speech_balloon:"

    value_str = config[ctx.guild.id]
    if value_str and config.config_type == ConfigType.USER:
        value_str = f'<@{value_str}>'
    elif value_str and config.config_type == ConfigType.CHANNEL:
        value_str = f'<#{value_str}>'

    description += f'{value_emoji} {value_str}\n'
    return description
