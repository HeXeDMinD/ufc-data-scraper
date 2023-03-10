from dataclasses import asdict
from json import dumps


class DataModelBase:
    def as_dict(self):
        return asdict(self)

    def as_json(self):
        return dumps(self.as_dict(), default=str)
