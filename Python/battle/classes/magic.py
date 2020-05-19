import random
from classes.game import bcolors

class Spell:
    def __init__(self, name, cost, dmg, type):
        self.name = bcolors.BOLD + bcolors.OKBLUE + name + bcolors.ENDC
        self.cost = cost
        self.dmg = dmg
        self.type = type

    def generate_damage(self):
        low = self.dmg - 15
        high = self.dmg + 15
        return random.randrange(low, high)
