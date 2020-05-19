import random


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    LightCyan = "\033[96m"


class Person:
    def __init__(self, name, hp, mp, atk, df, mgc, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.mgc = mgc
        self.items = items
        self.action = ["Attack", "Magic", "Items"]

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp
    
    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print(bcolors.OKBLUE + bcolors.BOLD + "    ACTIONS" + bcolors.ENDC)
        for item in self.action:
            print("        " +str(i)  + ":", item)
            i += 1

    def choose_mgc(self):
        x = 1
        print(bcolors.OKBLUE + bcolors.BOLD + "    MAGIC" + bcolors.ENDC)
        for spell in self.mgc:
            print("        " +str(x) + ":", spell.name, "(cost:", str(spell.cost) + ")")
            x+=1

    def choose_item(self):
        x = 1
        print(bcolors.OKGREEN + bcolors.BOLD + "    ITEMS:" + bcolors.ENDC)
        for item in self.items:
            print("        " +str(x) + ".", item["item"].name + ":", item["item"].description+ " (x"+str(item["quantity"])+ ")")
            x += 1

    def choose_target(self, enemies):
        if len(enemies) == 1:
            choice = 0
        else:
            i = 1
            print("\n" + bcolors.FAIL + bcolors.BOLD + "    TARGETS:" + bcolors.ENDC)
            for enemy in enemies:
                print("        " + str(i) + ".", enemy.name)
                i += 1
            choice = int(input("    Choose target:"))-1
        return choice

    def lowest_cost_spell(self):
        min_cost = 9999
        for spell in self.mgc:
            if spell.cost < min_cost:
                min_cost = spell.cost
        return min_cost

    def items_avaliable(self):
        default = False
        for item in self.items:
           if item["quantity"] > 0:
               default = True

        return default


    def choose_enemy_spell(self):
        mgc_choice = random.randrange(0, len(self.mgc))
        spell = self.mgc[mgc_choice]
        mgc_dmg = spell.generate_damage()
        pct = self.hp/self.maxhp

        if self.mp < spell.cost or spell.type == "white" and pct > 60:
            self.choose_enemy_spell()
        else:
            return spell, mgc_dmg

    def choose_enemy_item(self):
        #health - 0, mana - 1, dmg - 2
        pcth = self.hp/self.maxhp
        pctm = self.mp/self.maxmp

        item_choice = random.randrange(0, len(self.items))
        notchosen = True

        while notchosen:
            if item_choice == 0 and pcth > 0.7:
                item_choice = random.randrange(0, len(self.items))
                continue

            if item_choice == 1 and pctm > 0.7:
                item_choice = random.randrange(0, len(self.items))
                continue

            if not self.items[item_choice]["quantity"] > 0:
                # item_choice = random.randrange(0, len(self.items))
                item = None
                prop = None
                break

            self.items[item_choice]["quantity"] -= 1
            item = self.items[item_choice]["item"]
            prop = item.prop
            notchosen = False

        return item, prop, notchosen

    def death(self, enemies):
        deathcheck = ""
        if self.hp == 0:
            deathcheck = self.name
            enemies.remove(self)
        return deathcheck


    def get_enemy_stats(self):
        hp_bar = ""
        bar_ticks = (self.hp / self.maxhp * 100 / 2)

        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += " "


        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 11:
            decreased = 11 - len(hp_string)

            while decreased > 0:
                current_hp += " "
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        print("                      __________________________________________________ ")
        print(bcolors.BOLD + self.name +  "   "  + current_hp +" |" + bcolors.FAIL
              + hp_bar + bcolors.ENDC + bcolors.BOLD + "|     ")



    def get_stats(self):
        hp_bar = ""
        hp_bar_ticks = (self.hp / self.maxhp) * 100 / 4

        mp_bar = ""
        mp_bar_ticks = (self.mp / self.maxmp) * 100 / 10

        while hp_bar_ticks > 0:
            hp_bar += "█"
            hp_bar_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        while mp_bar_ticks > 0:
            mp_bar += "█"
            mp_bar_ticks -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 9:
            decreased = 9 - len(hp_string)

            while decreased > 0:
                current_hp += " "
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        mp_string = str(self.mp) + "/" + str(self.maxmp)
        current_mp = ""

        if len(mp_string) < 7:
            decreased = 7 - len(mp_string)

            while decreased > 0:
                current_mp += " "
                decreased -= 1

            current_mp += mp_string
        else:
            current_mp = mp_string



        print("                      _________________________               __________ ")
        print(bcolors.BOLD + self.name + "     " + current_hp + " |" + bcolors.OKGREEN
              + hp_bar + bcolors.ENDC + bcolors.BOLD + "|     "
              + current_mp + " |" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + "|")
