from core.models import Creature


class CombatResolver:
    def resolve(self, predator: Creature, prey: Creature) -> str:
        while predator.is_alive() and prey.is_alive():
            pred_dmg = predator.get_attack_power()
            prey_dmg = prey.get_attack_power()

            prey.take_damage(pred_dmg)
            predator.take_damage(prey_dmg)

        if not predator.is_alive():
            return "Pray ran into infinity"
        return "Some R-rated things have happened"
