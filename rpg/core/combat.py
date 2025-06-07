from rpg.utils.auxiliar_func import clear
from rpg.utils.dice_system import dice

from rpg.models.character import Character
from rpg.models.entity import Entity
from rpg.view.combat_view import show_combat_status

class CombatController:

    @classmethod
    def duel(cls, main_char: Character, enemy: Character | Entity) -> Character:
        combatants = [main_char, enemy]
        order = sorted(combatants, key=lambda c: c.roll_initiative(), reverse=True)
        print(f"Iniciativa definida! Ordem: {', '.join(c.name for c in order)}")

        round_count = 1
        while all(c.hp_current > 0 for c in combatants):
            clear()
            show_combat_status(main_char, enemy)
            print(f"\n🎲 === Round {round_count} ===")
            for actor in order:
                if actor.hp_current <= 0:
                    continue  # skip se estiver morto

                actor.apply_status_effects() 
                if "stunned" in actor.states:
                    print(f"😵 {actor.name} está atordoado e perde o turno!")
                    continue

                enemies = [c for c in combatants if c is not actor and c.hp_current > 0]
                if not enemies:
                    break
                target = enemies[0]

                if actor == main_char:
                    cls._player_turn(actor, target)
                else:
                    cls._enemy_turn(actor, target)

                if target.hp_current <= 0:
                    print(f"💀 {target.name} foi derrotado!")
            round_count += 1

        vencedor = max(combatants, key=lambda c: c.hp_current)
        input(f'\n🏆 {vencedor.name} venceu o duelo! Pressione ENTER para sair...')
        return vencedor

    @classmethod
    def _player_turn(cls, actor: Character, target: Entity) -> None:
        print(f"🎮 Seu turno, {actor.name}! ({actor.hp_current}/{actor.hp_max} HP)")

        while True:
            print("Escolha uma ação:")
            print("1. Atacar")
            print("2. Defender")
            choice = input("> ")

            if choice == "1":
                cls._resolve_attack(actor, target)
                break
            elif choice == "2":
                actor.defend()
                print(f"🛡️ {actor.name} assume postura defensiva. +2 AC até próximo turno.")
                break
            else:
                print("Escolha inválida. Tente novamente.")

    @classmethod
    def _enemy_turn(cls, actor: Entity, target: Character) -> None:
        print(f"🤖 Turno de {actor.name}...")
        cls._resolve_attack(actor, target)

    @classmethod
    def _resolve_attack(cls, actor: Character, target: Entity) -> None:
        atk_roll, crit = actor.roll_attack()
        effective_ac = target.ac + 2 if "defending" in target.states else target.ac
        print(f'{actor.name} rola ataque: {atk_roll} vs Defesa: {effective_ac}')

        if crit == 'CRITICAL_SUCCESS':
            print("💥 Crítico! Dano dobrado.")
            dmg = cls.compute_damage(actor, target) * 2
            target.take_damage(dmg)
        elif crit == 'CRITICAL_FAILURE':
            print("😬 Falha crítica! O ataque foi patético.")
        elif atk_roll > effective_ac:
            dmg = cls.compute_damage(actor, target)
            target.take_damage(dmg)
            print(f'{actor.name} acerta {target.name} e causa {dmg} de dano! ({target.hp_current}/{target.hp_max} HP restante)')
        else:
            print(f'{target.name} bloqueia o ataque!')

    @staticmethod
    def compute_damage(attacker: Character, defender: Character) -> int:
        raw = dice.roll(f'{attacker.main_weapon.base_dmg}+{attacker.prof_bonus}')['result']
        multiplier = defender.resistances.get(attacker.main_weapon.dmg_type, 1.0)
        return max(1, int(raw * multiplier))
