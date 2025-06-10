from dataclasses import dataclass
from random import randint


@dataclass(frozen=True)
class Equipment:
    name: str
    title: str
    slot: str
    base_dmg: int = 1
    dmg_type: str = "bludgeoning"
    proficience_mod: str = "strength"

    def is_weapon(self) -> bool:
        return self.slot in ("main_hand", "off_hand")

    def damage_roll(self) -> int:
        """Return randomized damage with ±20% variance"""
        variance = int(self.base_dmg * 0.2)
        return randint(self.base_dmg - variance, self.base_dmg + variance)

    def asdict(self) -> dict:
        item = {
            "name": self.name,
            "slot": self.slot,
        }
        if self.title:
            item["title"] = self.title
        if self.is_weapon():
            item.update({
                "base_dmg": self.base_dmg,
                "dmg_type": self.dmg_type,
                "proficience_mod": self.proficience_mod,
            })
        return item

    def __repr__(self):
        return f"{self.name}{f' ({self.title})' if self.title else ''}"


# Singleton vazio
EMPTY_SLOT = Equipment(name="Nothing", title="", slot="none", base_dmg=0, dmg_type="", proficience_mod="strength")
