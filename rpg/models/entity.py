from rpg.packages import ATTR_NAMES
from rpg.utils.dice_system import dice
from rpg.models.attributes import Attributes, CombatStats

class Entity:
    def __init__(self, name: str, title: str, level: int, attributes: dict, base_hp: int = 10):

        self.name = name
        self.title = title
        self.level = level
        self._attributes = Attributes(attributes)
        
        attrs = self.attributes.to_dict()
        self._prof_bonus = 0
        self._combat_stats = CombatStats(level, attrs, base_hp)
        self._resistances = {}
        self._states = {}

    @property
    def prof_bonus(self) -> int:
        return self._prof_bonus

    @property
    def alive(self) -> bool:
        return self._combat_stats.is_alive()
    
    @property
    def hp_max(self) -> int:
        return self._combat_stats.hp_max
    
    @property
    def hp_current(self) -> int:
        return self._combat_stats.hp_current
    
    @property
    def ac(self) -> int:
        return self._combat_stats.ac
    
    @property
    def attributes(self) -> Attributes:
        return self._attributes
    
    @property
    def resistances(self) -> dict[str, float]:
        return self._resistances
    
    @property
    def states(self) -> dict[str, int]:
        return self._states
    
    @property
    def dex_bonus(self) -> str:
        return self.get_attr_bonus('dexterity')
    
    def get_attr(self, attr: str) -> int:
        if attr not in ATTR_NAMES:
            raise ValueError(f"Invalid attribute: {attr}")
        return self.attributes.values[attr]
    
    def get_attr_bonus(self, attr: str) -> int:
        if attr not in ATTR_NAMES:
            raise ValueError(f"Invalid attribute: {attr}")
        return self.attributes.get_attr_bonus().get(attr, 0)

    def take_damage(self, amount: int) -> None:
        self._combat_stats.take_damage(amount)

    def heal(self, amount: int) -> None:
        self._combat_stats.heal(amount)

    def roll_initiative(self) -> int:
        return dice.roll(f'1d20+{self.dex_bonus}')['result']

    def roll_attack(self) -> tuple[int, int]:
        roll = dice.roll(f'1d20+{self.prof_bonus}', possible_crit=True)
        return roll['result'], roll['crit'], 

    def apply_status_effects(self):
        for state in list(self.states.keys()):
            turns = self.states[state]
            if state == "bleeding":
                self.take_damage(1)
                print(f"💉 {self.name} sangra e perde 1 HP!")
            elif state == "defending":
                print(f"{self.name} está em postura defensiva.")
            # outros estados aqui

            # decrementa turnos
            self.states[state] -= 1
            if self.states[state] <= 0:
                del self.states[state]

    # ACTIONS
    def defend(self):
        self.states["defending"] = 1
