from dataclasses import dataclass
from typing import Dict, Optional, TYPE_CHECKING

from royaleapi.models.base import CRObject

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass(eq=False)
class PlayerLeagueSeason(CRObject):
    trophies: int
    rank: Optional[int] = None

    # Can only be given in current_season and previous_season
    best_trophies: Optional[int] = None

    # Can only be given in previous_season and best_season
    season_id: Optional[str] = None

    @classmethod
    def de_json(cls, data: Dict, client: "RoyaleAPIClient") -> Optional["PlayerLeagueSeason"]:
        if not data:
            return None
        data = super().de_json(data, client)
        if "id" in data:
            data["season_id"] = data.pop("id")
        return cls(**data)
