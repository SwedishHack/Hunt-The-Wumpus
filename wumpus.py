# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 2023
author: SwedishHack
berglundgary@gmail.com
GPL. v3.0
"""
import argparse
import random
import sys

# cave description index definitions:
# leads to cave n,n,n [number]
index_cave1 = 0
index2_cave = 1
index_cave3 = 2
# contains wumpus [bool]
index_wumpus = 3
# contains pit [bool]
index_pit = 4
# contains bats [bool]
index_bat = 5


class MakeCaves:

    def __init__(self, num_caves):
        base_cave = [0, 0, 0, False, False, False]
        #FIXME: something is wrong with next line, because I have to do the 
                # loop to initial it properly
        self.location = [base_cave] * (num_caves + 1) 
        for acave in range(num_caves + 1):
            self.location[acave] = [0, 0, 0, False, False, False]

        # connect the caves
        if num_caves == 20:
            self.location[1] = [2, 5, 8, False, False, False]
            self.location[2] = [1, 3, 10, False, False, False]
            self.location[3] = [2, 4, 12, False, False, False]
            self.location[4] = [3, 5, 14, False, False, False]
            self.location[5] = [1, 4, 6, False, False, False]
            self.location[6] = [5, 7, 15, False, False, False]
            self.location[7] = [6, 8, 17, False, False, False]
            self.location[8] = [1, 7, 9, False, False, False]
            self.location[9] = [8, 10, 18, False, False, False]
            self.location[10] = [2, 9, 11, False, False, False]
            self.location[11] = [10, 12, 19, False, False, False]
            self.location[12] = [3, 11, 13, False, False, False]
            self.location[13] = [12, 14, 20, False, False, False]
            self.location[14] = [4, 13, 15, False, False, False]
            self.location[15] = [6, 14, 16, False, False, False]
            self.location[16] = [15, 17, 20, False, False, False]
            self.location[17] = [7, 16, 18, False, False, False]
            self.location[18] = [9, 17, 19, False, False, False]
            self.location[19] = [11, 18, 20, False, False, False]
            self.location[20] = [13, 16, 19, False, False, False]
        else:
            for cave_tunnel in range(3):
                for acave in range(1, num_caves + 1):
                    for attempt in range(100):
                        rand_cave = random.randrange(1, num_caves + 1)
                        if (self.location[rand_cave][cave_tunnel] == 0 and 
                                rand_cave != acave):
                            self.location[acave][cave_tunnel] = rand_cave
                            self.location[rand_cave][cave_tunnel] = acave
                            break
                    
                    # failed to find a path
                    if self.location[rand_cave][cave_tunnel] == 0:
                        print('\n***\nHelp, I could not build the caves.')
                
        # randomly place wumpus
        rand_cave = random.randrange(num_caves + 1)
        self.location[rand_cave][index_wumpus] = True

        # randomly place pits
        pits_placed = 0
        num_pits = 2
        while pits_placed < num_pits:
            rand_cave = random.randrange(num_caves + 1)
            # check for wumpus
            if (self.location[rand_cave][index_wumpus] == False and
                    self.location[rand_cave][index_pit] == False):
                self.location[rand_cave][index_pit] = True
                pits_placed += 1

        # randomly place bats
        bats_placed = 0
        num_bats = 2
        while bats_placed < num_bats:
            rand_cave = random.randrange(num_caves + 1)
            # check for wumpus
            if (self.location[rand_cave][index_wumpus] == False and
                    self.location[rand_cave][index_pit] == False and
                    self.location[rand_cave][index_bat] == False):
                self.location[rand_cave][index_bat] = True
                bats_placed += 1
                
    def situation(self, cave_location):
        # where am i?
        print('\nYou are in room {}.'.format(cave_location))
        
        # is wumpus here?
        if (self.location[cave_location][index_wumpus]):
            wumpus_action = random.choice(['fight','flight','flight'])
            if wumpus_action == 'fight':
                print('\tYou startle the wumpus and it kills you.')
                return 0
            else:
                print('\tYou startle the wumpus and it runs away.')
                
        # is pit here?
        if (self.location[cave_location][index_pit]):
            print('\tYou fell in a pit.')
            return 0
        
        # is bat here?
        if (self.location[cave_location][index_bat]):
            # randomly place player
            player_location = 0
            while player_location == 0:
                rand_cave = random.randrange(len(self.location))
                # check for wumpus, pit and bat
                if (self.location[rand_cave][index_wumpus] == False and
                        self.location[rand_cave][index_pit] == False and
                        self.location[rand_cave][index_bat] == False and 
                        cave_location != rand_cave):
                    player_location = rand_cave
            cave_location = player_location
            print('\tThere is a bat! It carries you off!\n')
            print('\nYou are in room {}.'.format(cave_location))
        
        # where can i go?
        cave1 = self.location[cave_location][index_cave1]
        cave2 = self.location[cave_location][index2_cave]
        cave3 = self.location[cave_location][index_cave3]
        print('Tunnels lead to {}, {}, {}.'.format(cave1, cave2, cave3))
        
        # smell[wumpus]
        if (self.location[cave1][index_wumpus] or
                self.location[cave2][index_wumpus] or
                self.location[cave3][index_wumpus]) :
            print('\tI smell a wumpus')
            
        # feel[pit]
        if (self.location[cave1][index_pit] or
                self.location[cave2][index_pit] or
                self.location[cave3][index_pit]) :
            print('\tI feel a draft.')
            
        # hear[bat]
        if (self.location[cave1][index_bat] or
                self.location[cave2][index_bat] or
                self.location[cave3][index_bat]) :
            print('\tI hear a bat.')
            
        return cave_location
    
    def player_start_loc(self, num_caves):
        player_location = 0
        while player_location == 0:
            rand_cave = random.randrange(num_caves + 1)
            # check for wumpus
            cave1 = self.location[rand_cave][index_cave1]
            cave2 = self.location[rand_cave][index2_cave]
            cave3 = self.location[rand_cave][index_cave3]
            if (self.location[rand_cave][index_wumpus] == False and
                    self.location[rand_cave][index_pit] == False and
                    self.location[rand_cave][index_bat] == False and
                    self.location[cave1][index_wumpus] == False and
                    self.location[cave2][index_wumpus] == False and
                    self.location[cave3][index_wumpus] == False):
                player_location = rand_cave
        return player_location
            
    def player_move(self, player_location):
        user_move = 0
        cave1 = self.location[player_location][index_cave1]
        cave2 = self.location[player_location][index2_cave]
        cave3 = self.location[player_location][index_cave3]
        while user_move == 0:
            user_response = input('Where to? ({}-{}-{}) '.format(cave1, cave2, cave3))
            if user_response.isdigit():
                user_response = int(user_response)
                if user_response in [cave1, cave2, cave3]:
                    user_move = user_response
        return user_move
    
    def player_shoot(self, player_location):
        user_shoot_distance = 0
        while user_shoot_distance == 0:
            user_response = input('Shoot how far? (1-5) ')
            if user_response.isdigit():
                user_response = int(user_response)
                if user_response in range(1,6):
                    user_shoot_distance = user_response
        
        user_shoot_cave = 0
        cave1 = self.location[player_location][index_cave1]
        cave2 = self.location[player_location][index2_cave]
        cave3 = self.location[player_location][index_cave3]
        while user_shoot_cave == 0:
            user_response = input('Where to? ({}-{}-{}) '.format(cave1, cave2, cave3))
            if user_response.isdigit():
                user_response = int(user_response)
                if user_response in [cave1, cave2, cave3]:
                    user_shoot_cave = user_response
        
        arrow_travel = 1
        while arrow_travel <= user_shoot_distance:
            if self.location[user_shoot_cave][index_wumpus] == True:
                print('You got the wumpus!')
                return -1
                
            elif user_shoot_cave == player_location:
                print('\tYou were hit by an arrow!')
                return 0
                
            elif arrow_travel < user_shoot_distance:
                print('\tArrow ricochets!')
                cave1 = self.location[user_shoot_cave][index_cave1]
                cave2 = self.location[user_shoot_cave][index2_cave]
                cave3 = self.location[user_shoot_cave][index_cave3]
                user_shoot_cave = random.choice([cave1, cave2, cave3])
            arrow_travel += 1
    
def play_game(num_caves):
    
    play_again = True
    
    while play_again == True:
        wumpus_killed = False
        player_arrows = 5
        caves = MakeCaves(num_caves)
        
        # randomly place player
        player_location = caves.player_start_loc(num_caves)
        
        # player turn
        while player_location != 0 and wumpus_killed == False:
            player_location = caves.situation(player_location)
            
            # what to do
            if player_location != 0:
                user_response = ''
                while (user_response != 's' and 
                       user_response != 'm' and
                       user_response != 'q'):
                    user_response = input('Shoot or Move (S-M) ').lower()
                
                # move
                if user_response == 'm':
                    player_location = caves.player_move(player_location)
                
                # shoot
                elif user_response == 's':
                    if player_arrows == 0:
                        print('\tYou have no arrows left!')
                        break
                    else:
                        player_arrows -= 1
                        
                        shoot_result = caves.player_shoot(player_location)
                    
                    if shoot_result == 0:
                        player_location = 0
                    elif shoot_result == -1:
                        wumpus_killed = True                    
                    
                    if player_location != 0 and wumpus_killed == False:
                        print('You have {} arrows left.'.format(player_arrows))
                        
                # quit
                elif user_response == 'q':
                    sys.exit()
                    
            # print('\n\nDM kills you')
            # player_location = 0
        
        if player_location == 0:
            print('\nYou are dead\n\nDo you want to play again?')
        else:
            print('The wumpus will get you next time.\n')
        user_response = ''
        while (user_response != 'y' and 
               user_response != 'n' and
               user_response != 'q'):
            user_response = input('Do you want to play again? (Y-N) ').lower()
        
        if user_response != 'y':
            play_again = False

if __name__ == "__main__":
    prog_name = 'wumpus'
    descript_msg = '''
    Hunt the Wumpus, by Gregory Yob, is a text-based adventure game set in a 
    series of caves connected by tunnels. The caves are in complete darkness, 
    so the player cannot see into adjacent caves. In one of the twenty caves 
    is a "Wumpus", which the player is attempting to kill. Additionally, 
    two of the caves contain bottomless pits, while two others contain 
    "super bats" which will pick up the player and move them to a random 
    cave. The game is turn-based; each cave is given a number by the game, 
    and each turn begins with the player being told which cave they are in 
    and which caves are connected to it by tunnels. The player then elects 
    to either move to one of those connected caves or shoot one of their 
    five "crooked arrows", named for their ability to change direction while 
    in flight and travel through several caves.
    From https://en.wikipedia.org/wiki/Hunt_the_Wumpus
    '''

    parser = argparse.ArgumentParser(prog=prog_name, description=descript_msg)
    
    
    # group = parser.add_mutually_exclusive_group(required=True)
    
    # help_msg = '''The original layout for Hunt the Wumpus has 20 caves in a dodecahedron connection pattern.
    # '''
    
    # group.add_argument('-o', '--original_layout',
    #                     type=bool,
    #                     default=True,
    #                     choices=[True, False],
    #                     help=help_msg
    #                     )
    
    help_msg = '''Player can choose the number of caves, 20, 40, 60. A size 
    of 20 will be the same as original game in a dodecahedron connection 
    pattern. Larger than default will make game longer and more difficult
    '''
    
    parser.add_argument('-n', '--num_caves',
                        type=int,
                        default=20,
                        choices=range(20, 61, 20),
                        help=help_msg)
    
    args = parser.parse_args()

    play_game(args.num_caves)
