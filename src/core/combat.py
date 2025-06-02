import random
from src.models.character import Character

def attack_roll(attacker: Character) -> int:
    # Exemplo: d20 + bônus de força
    bonus = attacker.get_bonus_attr("strength")
    return random.randint(1, 20) + bonus

def defense_roll(defender: Character) -> int:
    # Exemplo: d20 + bônus de destreza
    bonus = defender.get_bonus_attr("dexterity")
    return random.randint(1, 20) + bonus

def compute_damage(attacker: Character) -> int:
    # Dano simples = 1 + bônus de força (mínimo 1)
    bonus = attacker.get_bonus_attr("strength")
    return max(1, 1 + bonus)

def simple_duel(p1: Character, p2: Character):
    attacker, defender = p1, p2
    print(f"🔹 Iniciando duelo entre {p1.name} e {p2.name} 🔹")
    while p1.hp_current > 0 and p2.hp_current > 0:
        atk_roll = attack_roll(attacker)
        def_roll = defense_roll(defender)
        print(f"{attacker.name} rola ataque: {atk_roll} vs Defesa de {defender.name}: {def_roll}")
        if atk_roll > def_roll:
            dmg = compute_damage(attacker)
            defender.take_damage(dmg)
            print(f"⚔️  {attacker.name} acerta {defender.name} e causa {dmg} de dano! ({defender.hp_current}/{defender.hp_max} HP restante)")
        else:
            print(f"🛡️  {defender.name} bloqueia o ataque!")

        # Troca turno
        attacker, defender = defender, attacker  

    vencedor = p1 if p1.hp_current > 0 else p2
    input(f"🏆 {vencedor.name} venceu o duelo!")
    return vencedor
