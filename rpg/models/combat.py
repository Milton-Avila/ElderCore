from rpg.models.character import Character
from rpg.utils.dice_system import dice
class CombatController:
    @staticmethod
    def attack_roll(attacker: Character) -> int:
        # Exemplo: d20 + bônus de força
        bonus = attacker.get_bonus_attr('strength')
        return dice.roll(f'1d20+{bonus}')

    @staticmethod
    def defense_roll(defender: Character) -> int:
        # Exemplo: d20 + bônus de destreza
        bonus = defender.get_bonus_attr('dexterity')
        return dice.roll(f'1d20+{bonus}')
    
    @staticmethod
    def compute_damage(attacker: Character) -> int:
        # Dano simples = 1 + bônus de força (mínimo 1)
        base_dmg = attacker.base_dmg
        bonus = attacker.get_bonus_attr('strength')
        print(f'{base_dmg}+{bonus}')
        return dice.roll(f'{base_dmg}+{bonus}')

    @classmethod
    def simple_duel(cls, first_att: Character, second_att: Character) -> Character:
        attacker, defender = first_att, second_att
        while first_att.hp_current > 0 and second_att.hp_current > 0:
            atk_roll = cls.attack_roll(attacker)
            def_roll = cls.defense_roll(defender)
            print(f'{attacker.name} rola ataque: {atk_roll} vs Defesa de {defender.name}: {def_roll}')
            if atk_roll > def_roll:
                dmg = cls.compute_damage(attacker)
                defender.take_damage(dmg)
                print(f'⚔️  {attacker.name} acerta {defender.name} e causa {dmg} de dano! ({defender.hp_current}/{defender.hp_max} HP restante)')
            else:
                print(f'🛡️  {defender.name} bloqueia o ataque!')

            # Troca turno
            attacker, defender = defender, attacker  

        vencedor = first_att if first_att.hp_current > 0 else second_att
        input(f'🏆 {vencedor.name} venceu o duelo!')
        return vencedor
