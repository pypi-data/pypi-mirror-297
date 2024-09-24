from typing import Type, get_type_hints, TypeVar, Generic, Optional
from enum import Enum
from dataclasses import dataclass, is_dataclass
import json


# Type hinting (make life easier)
T = TypeVar('T', bound=dataclass)

# JSON Data Class Loader
class JSDC_Loader(Generic[T]):
    def __init__(self, data_path: str, data_class: Type[T]):
        if not is_dataclass(data_class): 
            raise ValueError('data_class must be a dataclass')
        
        self.data_path: str = data_path
        self.data: T = data_class() # Type hinting Supported
        self.load_data()

    def load_data(self, data_path: Optional[str] = None, encoding: str = 'utf-8') -> None:
        data_path = data_path if data_path is not None else self.data_path
        
        with open(data_path, 'r', encoding=encoding) as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                raise ValueError('not supported file format, only json is supported')

        for key, value in data.items():
            key = key.lower()
            if hasattr(self.data, key):
                if isinstance(value, dict):
                    _data = getattr(self.data, key)
                    self._update_nested_data(_data, value)
                else:
                    setattr(self.data, key, value)
            else:
                raise ValueError(f'unknown data key: {key}')

    def _update_nested_data(self, obj, data):
        type_hints = get_type_hints(type(obj))
        
        for sub_key, sub_value in data.items():
            if hasattr(obj, sub_key):
                expected_type = type_hints.get(sub_key)
                if isinstance(sub_value, dict):
                    sub_obj = getattr(obj, sub_key)
                    self._update_nested_data(sub_obj, sub_value)
                else:
                    if expected_type is not None:
                        try:
                            if issubclass(expected_type, Enum):
                                sub_value = expected_type[sub_value]
                            else:
                                sub_value = expected_type(sub_value)
                        except (ValueError, KeyError):
                            raise ValueError(f'invalid type for key {sub_key}, expected {expected_type}, got {type(sub_value)}')
                    setattr(obj, sub_key, sub_value)
            else:
                raise ValueError(f'unknown data key: {sub_key}')

    @staticmethod
    def dump_json(obj: T, output_path: str, encoding: str = 'utf-8', indent: int = 4):
        if not is_dataclass(obj):
            raise ValueError('obj must be a dataclass')
        
        data_dict = JSDC_Loader.__dataclass_to_dict(obj)
        with open(output_path, 'w', encoding=encoding) as f:
            json.dump(obj=data_dict, fp=f, indent=indent)

    @staticmethod
    def __dataclass_to_dict(obj: T):
        if isinstance(obj, Enum):
            return obj.name
        elif isinstance(obj, list):
            return [JSDC_Loader.__dataclass_to_dict(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            return {key: JSDC_Loader.__dataclass_to_dict(value) for key, value in vars(obj).items()}
        return obj

if __name__ == '__main__':
    from dataclasses import field
    from enum import auto
    @dataclass
    class DatabaseConfig:
        host: str = 'localhost'
        port: int = 3306
        user: str = 'root'
        password: str = 'password'

    # dump json
    data = DatabaseConfig()
    JSDC_Loader.dump_json(data, 'config.json')

    # load json
    loader = JSDC_Loader('config.json', DatabaseConfig)
    print(loader.data.host)

    @dataclass
    class UserType(Enum):
        ADMIN = auto()
        USER = auto()

    @dataclass
    class UserConfig:
        name: str = 'John Doe'
        age: int = 30
        married: bool = False
        user_type: UserType = field(default_factory=lambda: UserType.USER)

    @dataclass
    class AppConfig:
        user: UserConfig = field(default_factory=lambda: UserConfig())
        database: DatabaseConfig = field(default_factory=lambda: DatabaseConfig())

    data = AppConfig()
    # Prepare config.json / data.json
    JSDC_Loader.dump_json(data, 'config.json')

    loader = JSDC_Loader('config.json', AppConfig)
    print(loader.data.user.name)

    # update member
    loader.data.user.name = 'Jane Doe'
    JSDC_Loader.dump_json(loader.data, 'config.json')
    print(loader.data.user.name)

    # ControllerConfig
    @dataclass
    class ControllerConfig:
        controller_id: str = 'controller_01'
        controller_type: str = 'controller_type_01'
        controller_version: str = 'controller_version_01'
        utc_offset: float = 0.0
        app: AppConfig = field(default_factory=lambda: AppConfig())
    
    data = ControllerConfig()
    data.utc_offset = 9.0
    JSDC_Loader.dump_json(data, 'config.json')
    
    loader = JSDC_Loader('config.json', ControllerConfig)
    print(loader.data)

    # Clean up
    import os
    os.remove('config.json')
