from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, TYPE_CHECKING

from royaleapi.constants import ClanBattleType
from royaleapi.models.base import CRObject
from royaleapi.models.clan_badge import ClanBadge
from royaleapi.models.clan_tracking import ClanTracking
from royaleapi.models.location import Location

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient
    from royaleapi.models.battle import Battle
    from royaleapi.models.clan_war import ClanWar
    from royaleapi.models.player import Player


@dataclass
class Clan(CRObject):
    tag: str
    name: str = field(compare=False)

    # Most endpoints have this
    badge: Optional[ClanBadge] = field(default=None, compare=False)

    # Tournament endpoint only
    badge_id: Optional[int] = field(default=None, compare=False)

    # Clan endpoint only
    description: Optional[str] = field(default=None, compare=False)
    clan_type: Optional[str] = field(default=None, compare=False)
    score: Optional[int] = field(default=None, compare=False)  # Also in clan leaderboard endpoint
    war_trophies: Optional[int] = field(default=None, compare=False)  # Also in clan war endpoint
    member_count: Optional[int] = field(default=None, compare=False)  # Also in clan leaderboard endpoint
    required_score: Optional[int] = field(default=None, compare=False)
    total_donations: Optional[int] = field(default=None, compare=False)
    location: Optional[Location] = field(default=None, compare=False)  # Also in clan leaderboard endpoint
    # Not returned in "clan/search" endpoint
    members: List["Player"] = field(default_factory=list, compare=False)
    tracking: Optional[ClanTracking] = field(default=None, compare=False)

    # Player endpoint only
    role: Optional[str] = field(default=None, compare=False)
    player_donations: Optional[int] = field(default=None, compare=False)
    donations_received: Optional[int] = field(default=None, compare=False)
    donations_delta: Optional[int] = field(default=None, compare=False)

    # Clan war endpoint only
    participants: Optional[int] = field(default=None, compare=False)
    battles_played: Optional[int] = field(default=None, compare=False)
    wins: Optional[int] = field(default=None, compare=False)
    crowns: Optional[int] = field(default=None, compare=False)

    # Clan war log endpoint only
    war_trophies_change: Optional[int] = field(default=None, compare=False)

    # Clan leaderboard endpoint only
    rank: Optional[int] = field(default=None, compare=False)
    previous_rank: Optional[int] = field(default=None, compare=False)

    client: Optional["RoyaleAPIClient"] = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        from royaleapi.models.player import Player  # I did not want to do this
        self.badge = ClanBadge.de_json(self.badge, self.client)
        self.location = Location.de_json(self.location, self.client)
        self.members = Player.de_list(self.members, self.client)
        self.tracking = ClanTracking.de_json(self.tracking, self.client)

    def get_clan(self, use_cache: bool = True) -> "Clan":
        return self.client.get_clan(self.tag, use_cache=use_cache)

    def get_battles(self, battle_type: str = ClanBattleType.CLANMATE,
                    max_results: Optional[int] = None, page: Optional[int] = None,
                    use_cache: bool = True) -> List["Battle"]:
        return self.client.get_clan_battles(self.tag, battle_type, max_results, page, use_cache)

    def get_war(self, use_cache: bool = True) -> "ClanWar":
        return self.client.get_clan_war(self.tag, use_cache)

    def get_war_log(self, max_results: Optional[int] = None, page: Optional[int] = None,
                    use_cache: bool = True) -> List["ClanWar"]:
        return self.client.get_clan_war_log(self.tag, max_results, page, use_cache)

    def get_tracking(self, use_cache: bool = True) -> ClanTracking or List[ClanTracking]:
        return self.client.get_clan_tracking(self.tag, use_cache=use_cache)

    def track(self) -> bool:
        return self.client.track_clan(self.tag)

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["Clan"]:
        if not data:
            return None
        data = super().de_json(data, client)
        if "type" in data:
            data["clan_type"] = data.pop("type")
        if "donations" in data:
            if "role" in data:  # Clan object is from "player" endpoint
                data["player_donations"] = data.pop("donations")
            else:  # Clan object is from "clan" endpoint
                data["total_donations"] = data.pop("donations")
        return cls(client=client, **data)
