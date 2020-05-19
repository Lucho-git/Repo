from classes.game import bcolors


class Item:
    def __init__(self, name, type, description, prop):
        self.name = bcolors.BOLD + bcolors.LightCyan + name + bcolors.ENDC
        self.type = type
        self.description = description
        self.prop = prop
