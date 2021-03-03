from Classes.game import Person,bcolors
from Classes.magic import Spell
from Classes.inventory import Item
import random

#Create Black Magic
fire = Spell("Fire",25,600,"Black")
water = Spell("Water",25,600,"Black")
thunder = Spell("Thunder",25,600,"Black")
meteor = Spell("Meteor",40,1400,"Black")
quake = Spell("Quake",40,1400,"Black")
blizzard = Spell("Blizzard",50,1450,"Black")

#Create white Magic
cure = Spell("Cure",25,620,"White")
cura = Spell("Cura",50,1500,"White")

#Create Some Items
potion = Item("Potion", "potion","Heals 50 HP",50)
hpotion = Item("Hi-Potion", "potion","Heals 100 HP",100)
elixer = Item("Elixer", "elixer","Restores HP/MP of one party member",999)
grenade = Item("Grenade", "attack","Damages 500 damage", 500)

player_spell =[fire,thunder,blizzard,meteor,water,cure,cura]
enemy_spell = [fire,meteor,water,cure,blizzard]
player_items = [{"item":potion, "quantity": 15},{"item":hpotion, "quantity": 5},{"item":elixer, "quantity": 5},{"item":grenade, "quantity": 5}]

#Instantiate People
player1 = Person("Naruto:",4260,132,400,34,player_spell,player_items)
player2 = Person("Sasuke:",4160,163,400,34,player_spell,player_items)
player3 = Person("Sakura:",4060,174,500,34,player_spell,player_items)

enemy1 = Person("Obito   ",1500, 130, 560, 325,enemy_spell,[])
enemy2 = Person("Madara",11200,700,520,25,enemy_spell,[])
enemy3 = Person("Nagato  ",1250,130,560,325,enemy_spell,[])

players = [player1,player2,player3]
enemies = [enemy1,enemy2,enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS" + bcolors.ENDC)

while running:
    print("=============")
    print("Name              HP                                       MP")
    for player in players:
        player.get_stats()

    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("Choose action:")
        index = int(choice) - 1
        #print("You choose", choice)

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ","") + " for" ,dmg,"points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ","") + " has died.")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose Magic:"))-1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "Not enough MP" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "White":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg),"HP" + bcolors.ENDC)
            elif spell.type == "Black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "damage point to " + enemies[enemy].name.replace(" ","") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ","") + " has died.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_items()
            item_choice = int(input("Choose item")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n " + "None Left" + bcolors.ENDC)
                continue

            player.item[item_choice]["quantity"] -= 1

            if item.type =="potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN+ "\n" + item.name + "heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":
                player.hp=player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + "Fully Restored HP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].choose_target(item.prop)
                print(bcolors.FAIL + "\n" + item.name + "Deals" , str(item.prop), "points of damage to "+enemies[enemy].name+ bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ","") + " has died.")
                    del enemies[enemy]

    #Check if battel is over
    defeated_enemies = 0
    defeated_player = 0

    for player in players:
        if player.get_hp() == 0:
            defeated_player += 1

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    #Check if player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You Win" + bcolors.ENDC)
        running = False
    #Check if Enemy won
    elif defeated_player == 2:
        print(bcolors.FAIL + "Enemy defeated you" + bcolors.ENDC)
        running = False

    #Enemy attack Phase
    for enemy in enemies:
        enemy_choice = random.randrange(0,2)
        if enemy_choice == 0:
            #Chose Attack
            target = random.randrange(0,3)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacks" + players[target].name.replace(" ","") + " for",enemy_dmg)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "White":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals"+ enemy.name +"for", str(magic_dmg),"HP" + bcolors.ENDC)

            elif spell.type == "Black":
                target = random.randrange(0,3)
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ","") + "'s " + spell.name +" deals" , str(magic_dmg), "damage point to " + players[target].name.replace(" ","") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ","") + " has died.")
                    del players[player]
            #print("Enemy chose", spell, "damage is", magic_dmg)





