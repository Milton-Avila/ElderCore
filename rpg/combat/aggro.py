class AggroSystem:
    def __init__(self):
        self.threat = {}

    def update_threat(self, attacker, target, value):
        self.threat.setdefault(target, 0)
        self.threat[target] += value

    def get_primary_target(self, enemy_team):
        return max(enemy_team, key=lambda e: self.threat.get(e, 0), default=enemy_team[0])
