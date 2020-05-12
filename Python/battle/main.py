from classes.game import Person, bcolors

mgc = [{"name": "Fire", "cost": 10, "dmg": 100},
       {"name": "Thunder", "cost": 10, "dmg": 124},
       {"name": "Blizzard", "cost": 10, "dmg": 100}]

player = Person(460, 65, 60, 34, mgc)
enemy = Person(1200, 65, 45, 25, mgc)

running = True
i = 0
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
       print("========================")
       player.choose_action()
       choice = input("Choose action:")
       index = int(choice) -1

       if index == 0:
              dmg = player.generate_damage()
              enemy.take_damage(dmg)
              print("You attacked for", dmg, "points of damage. Enemy HP:", enemy.get_hp())
       elif index == 1:
              player.choose_mgc()
              mgc_choice = int(input("Choose magic:")) - 1
              mgc_dmg = player.generate_spell_damage(mgc_choice)
              spell = player.get_spell_name(mgc_choice)
              cost = player.get_spell_mp_cost(mgc_choice)

              current_mp = player.get_max_mp()

              if cost > player.get_mp():
                     print(bcolors.FAIL + "\nNot Enough MP!\n" + bcolors.ENDC)
                     continue

              player.reduce_mp(cost)
              enemy.take_damage(mgc_dmg)

              print(bcolors.OKBLUE + "\n"+spell,"deals", str(mgc_dmg), "points of damage" + bcolors.ENDC)

       enemy_choice = 1

       enemy_dmg = enemy.generate_damage()
       player.take_damage(enemy_dmg)
       print("Enemy attacks for", enemy_dmg)
       print("__________________________")
       print("Enemy HP:", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC)
       print("__________________________")
       print("Your HP:", bcolors.OKGREEN + str(player.get_hp()) + "/" + str(player.get_max_hp()) + bcolors.ENDC)
       print("Your HP:", bcolors.OKBLUE + str(player.get_mp()) + "/" + str(player.get_max_mp()) + bcolors.ENDC)


       if enemy.get_hp == 0:
              print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
              running = False
       elif player.get_hp() == 0:
              print(bcolors.FAIL + "The Enemy has defeated you!")
              running = False
