from typing import Any, Dict


class VulnLoader:
    '''
    Мета-класс для создания структуры уязвимости на основе конфигурационного файла
    '''
    def __init__(self, data: Dict[str, Any]):
        self.affected = []
        for key, value in data.items():
            if isinstance(value, dict):
                if 'value' in value and 'settings' in value:
                    setattr(self, key, value['value'])
                    setattr(self, f"{key}_settings", value['settings'])
                else:
                    setattr(self, key, VulnLoader(value))
            elif isinstance(value, list):
                setattr(self, key, [VulnLoader(item) if isinstance(item, dict) else item for item in value])
            else:
                setattr(self, key, value)

    def __repr__(self):
        return f"{self.__dict__}"

    def __getattr__(self, name: str) -> Any:
        if name in self.__dict__:
            return self.__dict__[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def get_key_by_value(self, target_value):

        for ups, val in self.__dict__.items():
            if type(val) is list:
                for value in val:
                    if value == target_value:
                        matching_keys = ups
            else:
                if val == target_value:
                    matching_keys = ups

        if len(matching_keys) == 1:
            return matching_keys[0]
        elif len(matching_keys) > 1:
            return matching_keys
        else:
            return None


class VulnBuilder(VulnLoader):
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)


class VulnManager:
    def __init__(self):
        self.dict_list = []

    def add_or_update_dict(self, identifier, new_data: Dict, ident):
        for existing_dict in self.dict_list:
            if existing_dict.get('id') == identifier:
                if type(existing_dict.get(ident)) is list:
                    new_dict = existing_dict.get(ident)
                    for m in new_dict:
                        new_data.get(ident).append(m)
                existing_dict.update(new_data)
                break
        else:
            new_data['id'] = identifier
            self.dict_list.append(new_data)

    def get_dicts(self):
        return self.dict_list
