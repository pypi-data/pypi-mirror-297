import orjson
from pydantic import BaseModel

from .helpers import orjson_dumps


class Model(BaseModel):
    @classmethod
    def is_type_dict(cls, field):
        return cls.model_fields[field]._attributes_set["annotation"] == dict

    @classmethod
    def from_record(cls, record):
        data = {
            k: (v if not v or not cls.is_type_dict(k) else orjson.loads(v))
            for k, v in record.items()
            if k in cls.model_fields
        }
        return cls(**data)

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        use_enum_values = True
