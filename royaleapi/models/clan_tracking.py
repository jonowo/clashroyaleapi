from dataclasses import dataclass

from royaleapi.models.base import CRObject


@dataclass(eq=False)
class ClanTracking(CRObject):
    active: bool
    available: bool
    snapshot_count: int

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super().de_json(data)
        return cls(**data)