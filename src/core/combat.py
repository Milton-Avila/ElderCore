from src.models.character import Character
from src.utils.dice_system import dice

def attack_roll(attacker: Character) -> int:
    # Exemplo: d20 + bônus de força
    bonus = attacker.get_bonus_attr('strength')
    return dice.roll(f'1d20+{bonus}')

def defense_roll(defender: Character) -> int:
    # Exemplo: d20 + bônus de destreza
    bonus = defender.get_bonus_attr('dexterity')
    return dice.roll(f'1d20+{bonus}')

def compute_damage(attacker: Character) -> int:
    # Dano simples = 1 + bônus de força (mínimo 1)
    bonus = attacker.get_bonus_attr('strength')
    return dice.roll(f'1d6+{bonus}')

def simple_duel(first_att: Character, second_att: Character) -> Character:
    attacker, defender = first_att, second_att
    while first_att.hp_current > 0 and second_att.hp_current > 0:
        atk_roll = attack_roll(attacker)
        def_roll = defense_roll(defender)
        print(f'{attacker.name} rola ataque: {atk_roll} vs Defesa de {defender.name}: {def_roll}')
        if atk_roll > def_roll:
            dmg = compute_damage(attacker)
            defender.take_damage(dmg)
            print(f'⚔️  {attacker.name} acerta {defender.name} e causa {dmg} de dano! ({defender.hp_current}/{defender.hp_max} HP restante)')
        else:
            print(f'🛡️  {defender.name} bloqueia o ataque!')

        # Troca turno
        attacker, defender = defender, attacker  

    vencedor = first_att if first_att.hp_current > 0 else second_att
    input(f'🏆 {vencedor.name} venceu o duelo!')
    return vencedor
