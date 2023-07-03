from dataclasses import dataclass, asdict
from json import dumps


@dataclass(frozen=True, order=True)
class DataModelBase:
    def as_dict(self):
        return asdict(self)

    def as_json(self):
        return dumps(self.as_dict(), default=str)
