from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

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

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

#Create spell array
player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]

#Create item array
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 2},
                {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 1},
                {"item": grenade, "quantity": 5}]

#Instantiate People
player1 = Person("Valos:",3260, 132, 60, 34, player_spells, player_items)
player2 = Person("Nick :",4160, 188, 60, 34, player_spells, player_items)
player3 = Person("Robot:",3089, 174, 60, 34, player_spells, player_items)

#Instantiate Enemies
enemy1 = Person("Imp  ",1250, 130, 560, 325, [], [])
enemy2 = Person("Magus",12500, 221, 725, 25, [], [])
enemy3 = Person("Imp  ",1250, 130, 560, 325, [], [])


#Create player array
players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
       print("============================================================================")
       print("NAME                  HP                                      MP")
       for player in players:
              player.get_stats()
       print("\n============================================================================")
       for enemy in enemies:
              enemy.get_enemy_stats()
       print("\n============================================================================")

       for player in players:

              print("    "+player.name)
              player.choose_action()
              choice = input("    Choose action: ")
              index = int(choice) - 1

              if index == 0:
                     dmg = player.generate_damage()
                     enemy = enemies[player.choose_target(enemies)]
                     enemy.take_damage(dmg)
                     print(player.name, " attacked: " + enemy.name + " for", dmg,
                           "points of damage. Enemy HP:", enemy.get_hp())
                     deathcheck = enemy.death(enemies)
                     if deathcheck != "":
                            print("Enemy:", deathcheck, "has been killed by:", player.name)
                            if len(enemies) == 0:
                                   print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
                                   running = False

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
                            print(bcolors.OKBLUE + '\n' + spell.name, "heals for:", str(mgc_dmg),
                                  "points of HP" + bcolors.ENDC)

                     elif spell.type == "black":
                            enemy = enemies[player.choose_target(enemies)]
                            enemy.take_damage(mgc_dmg)
                            print(bcolors.OKBLUE + "\n" + spell.name, "deals", str(mgc_dmg),
                                  "points of damage to", enemy.name + bcolors.ENDC)

                            deathcheck = enemy.death(enemies)
                            if deathcheck != "":
                                   print("Enemy:", deathcheck, "has been killed by:", player.name)
                                   if len(enemies) == 0:
                                          print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
                                          running = False


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
                            print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
                     elif item.type == "elixer":
                            if item.name == "MegaElixer":
                                   for i in players:
                                          i.hp = i.maxhp
                                          i.mp = i.maxmp
                            else:
                                   player.hp = player.maxhp
                                   player.mp = player.maxmp
                            print(bcolors.OKGREEN + "\n", item.name, "fully restores HP/MP" + bcolors.ENDC)
                     elif item.type == "attack":
                            enemy = enemies[player.choose_target(enemies)]
                            enemy.take_damage(item.prop)
                            print(bcolors.FAIL + "\n", item.name, "deals", str(item.prop),
                                  "points of damage to", enemy.name + bcolors.ENDC)
                            deathcheck = enemy.death(enemies)
                            if deathcheck != "":
                                   print("Enemy:", deathcheck, "has been killed by:", player.name)
                                   if len(enemies) == 0:
                                          print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
                                          running = False
                                          continue



       enemy_choice = 1
       target = random.randrange(0, len(players))
       enemy_dmg = enemies[0].generate_damage()
       players[target].take_damage(enemy_dmg)
       print("Enemy attacks for", enemy_dmg)

       defeated_enemies = 0
       for enemy in enemies:
              if enemy.get_hp() == 0:
                     defeated_enemies += 1

       if defeated_enemies == len(enemies):
              print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
              running = False

       defeated_players = 0
       for player in players:
              if player.get_hp() == 0:
                     defeated_players += 1

       if defeated_players == len(players):
              print(bcolors.FAIL + "The Enemy has defeated you!")
              running = False
