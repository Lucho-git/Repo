from classes.game import Person, bcolors

mgc = [{"name": "Fire", "cost": 10, "dmg": 60},
       {"name": "Thunder", "cost": 10, "dmg": 60},
       {"name": "Blizzard", "cost": 10, "dmg": 60}]

player = Person(460, 65, 60, 34, mgc)
enemy = Person(1200, 65, 45, 25, mgc)

running = True
i = 0
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
       print("========================")
       player.choose_magic()
       choice = input("Choose action:")
       index = int(choice) -1

       if index == 0:
              dmg = player.generate_damage()
              enemy.take_damage(dmg)
              print("You attacked for", dmg, "points of damage. Enemy HP:", enemy.get_hp())

       enemy_choice = 1

       enemy_dmg = enemy.generate_damage()
       player.take_damage(enemy_dmg)
       print("Enemy attacks for", enemy_dmg, "Player HP:", player.get_hp())


       if enemy.get_hp == 0:
              print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
              running = False
       elif player.get_hp() == 0:
              print(bcolors.FAIL + "The Enemy has defeated you!")
              running = False
              