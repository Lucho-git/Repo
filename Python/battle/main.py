from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random
import copy

#Create Black Magic
fire = Spell("Fire", 20, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

#Create White Magic
cure = Spell("Cure", 20, 620, "white")
cura = Spell("Cura", 45, 1500, "white")

#Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 1000 damage", 1000)

#Create spell array
player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, cure]

#Create item array
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 2},
                {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 1},
                {"item": grenade, "quantity": 5}]

enemy_items = [{"item": superpotion, "quantity": 2},
               {"item": elixer, "quantity": 1},
               {"item": grenade, "quantity": 1}]

#Instantiate People
p1name = bcolors.OKGREEN + "Valos:" + bcolors.ENDC
p2name = bcolors.OKGREEN + "Nick :" + bcolors.ENDC
p3name = bcolors.OKGREEN + "Robot:" + bcolors.ENDC

player1 = Person(p1name, 3260, 132, 60, 34, player_spells, copy.copy(player_items))
player2 = Person(p2name, 4160, 188, 60, 34, player_spells, copy.copy(player_items))
player3 = Person(p3name, 3089, 174, 60, 34, player_spells, copy.copy(player_items))

e1name = bcolors.FAIL + "Imp   " + bcolors.ENDC
e2name = bcolors.FAIL + "Magus " + bcolors.ENDC
e3name = bcolors.FAIL + "Imp   " + bcolors.ENDC

#Instantiate Enemies
enemy1 = Person(e1name, 1250, 130, 560, 325, enemy_spells, copy.deepcopy(enemy_items))
enemy2 = Person(e2name, 12500, 221, 725, 25, enemy_spells, copy.deepcopy(enemy_items))
enemy3 = Person(e3name, 1250, 130, 560, 325, enemy_spells, copy.deepcopy(enemy_items))


#Create player array
players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:

       #Start Battle Sequence
       print("============================================================================")
       print("NAME                  HP                                      MP")
       for player in players:
              player.get_stats()
       print("\n============================================================================")
       for enemy in enemies:
              enemy.get_enemy_stats()
       print("\n============================================================================")

       #Players Turn
       for player in players:

              if not running:
                     continue

              print("    "+player.name)
              player.choose_action()
              choice = input("    Choose action: ")
              index = int(choice) - 1

              #Normal Attack
              if index == 0:
                     dmg = player.generate_damage()
                     enemy = enemies[player.choose_target(enemies)]
                     enemy.take_damage(dmg)
                     print(player.name, "attacked", enemy.name.replace(" ", ""), "for", dmg,
                           "points of damage.\n")
                     deathcheck = enemy.death(enemies)
                     if deathcheck != "":
                            print("Enemy", deathcheck.replace(" ", ""), "has been killed by", player.name + "\n")
                            if len(enemies) == 0:
                                   print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
                                   running = False
                                   continue

              #Magic Spell
              elif index == 1:
                     player.choose_mgc()
                     mgc_choice = int(input("Choose magic: ")) - 1

                     if mgc_choice == -1:
                            continue

                     #choose spell, generate the damage, check for enough mp to cast
                     spell = player.mgc[mgc_choice]
                     mgc_dmg = spell.generate_damage()
                     current_mp = player.get_max_mp()
                     if spell.cost > player.get_mp():
                            print(bcolors.FAIL + "\nNot Enough MP!\n" + bcolors.ENDC)
                            continue

                     player.reduce_mp(spell.cost)

                     #spell type determines its effects, choose target(s)
                     if spell.type == "white":
                            player.heal(mgc_dmg)
                            print(player.name, spell.name, "heals for:", str(mgc_dmg),
                                  "points of HP" + bcolors.ENDC + "\n")

                     elif spell.type == "black":
                            enemy = enemies[player.choose_target(enemies)]
                            enemy.take_damage(mgc_dmg)
                            print(player.name, spell.name, "deals", str(mgc_dmg),
                                  "points of damage to", enemy.name.replace(" ", "") + bcolors.ENDC + "\n")

                            deathcheck = enemy.death(enemies)
                            if deathcheck != "":
                                   print("Enemy", deathcheck.replace(" ", ""), "has been killed by", player.name + "\n")
                                   if len(enemies) == 0:
                                          print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
                                          running = False
                                          continue


              #Item Choice
              elif index == 2:
                     player.choose_item()
                     item_choice = int(input("Choose item: ")) - 1

                     if item_choice == -1:
                            continue

                     item = player.items[item_choice]["item"]
                     player.items[item_choice]["quantity"] -= 1

                     if player.items[item_choice]["quantity"] < 0:
                            player.items[item_choice]["quantity"] = 0
                            print(bcolors.FAIL + "You have run out of",
                                  player.items[item_choice]["item"].name + bcolors.ENDC)
                            continue

                     if item.type == "potion":
                            player.heal(item.prop)
                            print(player.name, item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC + "\n")
                     elif item.type == "elixer":
                            if item.name == "MegaElixer":
                                   for i in players:
                                          i.hp = i.maxhp
                                          i.mp = i.maxmp
                            else:
                                   player.hp = player.maxhp
                                   player.mp = player.maxmp
                            print(player.name, item.name, "fully restores HP/MP" + bcolors.ENDC + "\n")
                     elif item.type == "attack":
                            enemy = enemies[player.choose_target(enemies)]
                            enemy.take_damage(item.prop)
                            print(player.name, item.name, "deals", str(item.prop),
                                  "points of damage to", enemy.name.replace(" ", "") + bcolors.ENDC + "\n")
                            deathcheck = enemy.death(enemies)
                            if deathcheck != "":
                                   print("Enemy", deathcheck.replace(" ", ""), "has been killed by", player.name + "\n")
                                   if len(enemies) == 0:
                                          print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
                                          running = False
                                          continue

       print(bcolors.FAIL + "---Enemy Turn---" + bcolors.ENDC)

       #Enemies Turn
       for enemy in enemies:
              if not running:
                     continue

              choose_action = True
              enemy_choice = random.randrange(0, 3)
              while choose_action:
                     choose_action = False
                     if enemy_choice == 0:

                            target = random.randrange(0, len(players))
                            enemy_dmg = enemies[0].generate_damage()
                            players[target].take_damage(enemy_dmg)
                            print("\n" + enemy.name.replace(" ", ""), "attacks", players[target].name, "for", enemy_dmg)

                            deathcheck = players[target].death(players)
                            if deathcheck != "":
                                   print("\nAlly", deathcheck, "has been killed by", enemy.name.replace(" ", ""))
                                   if len(players) == 0:
                                          print(bcolors.FAIL + "\n\n""You have been Defeated!" + bcolors.ENDC)
                                          running = False

                     elif enemy_choice == 1:

                            mana_check = enemy.lowest_cost_spell()
                            if enemy.mp >= mana_check:
                                   spell, mgc_dmg = enemy.choose_enemy_spell()
                            else:
                                   enemy_choice = 2
                                   choose_action = True
                                   continue

                            if spell.type == "white":
                                   enemy.heal(mgc_dmg)
                                   print(bcolors.OKBLUE + '\n' + enemy.name.replace(" ", ""), "heals for:", str(mgc_dmg),
                                         "points of HP" + bcolors.ENDC)

                            elif spell.type == "black":
                                   target = random.randrange(0, len(players))
                                   players[target].take_damage(mgc_dmg)
                                   print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", ""), spell.name, "deals", str(mgc_dmg),
                                         "points of damage to", players[target].name + bcolors.ENDC)

                                   deathcheck = players[target].death(players)
                                   if deathcheck != "":
                                          print("\nAlly", deathcheck, "has been killed by", enemy.name.replace(" ", ""))
                                          if len(players) == 0:
                                                 print(bcolors.FAIL + "You have been Defeated!" + bcolors.ENDC)
                                                 running = False

                     elif enemy_choice == 2:
                            item = None
                            prop = None

                            if enemy.items_avaliable():
                                   item, prop, notchosen = enemy.choose_enemy_item()
                                   if notchosen:
                                          enemy_choice = 0
                                          choose_action = True
                                          continue
                            else:
                                   enemy_choice = 0
                                   choose_action = True
                                   continue

                            if item.type == "potion":
                                   enemy.heal(item.prop)
                                   print("\n" + enemy.name.replace(" ", "") + bcolors.WARNING, item.name + " heals",
                                         "for", str(prop), "HP" + bcolors.ENDC)
                            elif item.type == "elixer":
                                   if item.name == "MegaElixer":
                                          for i in enemies:
                                                 i.hp = i.maxhp
                                                 i.mp = i.maxmp
                                   else:
                                          enemy.hp = enemy.maxhp
                                          enemy.mp = enemy.maxmp
                                   print("\n", enemy.name.replace(" ", "") + bcolors.WARNING, item.name,
                                         "fully restores", enemy.name.replace(" ", ""), "HP/MP" + bcolors.ENDC)

                            elif item.type == "attack":
                                   target = random.randrange(0, len(players))
                                   players[target].take_damage(prop)
                                   print("\n" + enemy.name.replace(" ", ""), item.name, "deals", str(item.prop),
                                         "points of damage to", players[target].name + bcolors.ENDC)

                                   deathcheck = players[target].death(players)
                                   if deathcheck != "":
                                          print("\nAlly", deathcheck, "has been killed by", enemy.name.replace(" ", ""))
                                          if len(players) == 0:
                                                 print(bcolors.FAIL + "You have been Defeated!" + bcolors.ENDC)
                                                 running = False
       if running:
              print(bcolors.OKGREEN + "\n---Your Turn---\n" + bcolors.ENDC)

