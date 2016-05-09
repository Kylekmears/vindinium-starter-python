#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## TODO: Board to screen

import os
import sys
import requests
import re
from bot import RandomBot, SlowBot, Bot
import os
import platform


TIMEOUT=15

def return_board(jsonDict):
    board = jsonDict['game']['board']['tiles']
    size = jsonDict['game']['board']['size'] * 2 
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    
    total_gold = 0
    bank_ledger = {}
    out_board = ''
    seventh_line = ''
    hero_number = 1

    for i in range(4):
        if jsonDict['game']['heroes'][i]['name'] == 'karyote': #Change this for other characters!
            hero_number = i + 1
        total_gold += jsonDict['game']['heroes'][i]['gold']
        bank_ledger[i] = jsonDict['game']['heroes'][i]['gold']

    ledger_length = 25
    for j in range(4):
        if total_gold != 0:
            seventh_line += str(j+1) * int((bank_ledger[j]/total_gold)*ledger_length)
        else:
            seventh_line = '-' * ledger_length
        
    health_divisor = 4
    meta_data = {
        0: "     HEALTH",
        1: "    P1: " + '+'*(jsonDict['game']['heroes'][0]['life']//health_divisor) +
((100//health_divisor-(jsonDict['game']['heroes'][0]['life']//health_divisor))-1)*' '+'|',
        2: "    P2: " + '+'*(jsonDict['game']['heroes'][1]['life']//health_divisor) + 
((100//health_divisor-(jsonDict['game']['heroes'][1]['life']//health_divisor))-1)*' '+'|',
        3: "    P3: " + '+'*(jsonDict['game']['heroes'][2]['life']//health_divisor) + 
((100//health_divisor-(jsonDict['game']['heroes'][2]['life']//health_divisor))-1)*' '+'|',
        4: "    P4: " + '+'*(jsonDict['game']['heroes'][3]['life']//health_divisor) +
((100//health_divisor-(jsonDict['game']['heroes'][3]['life']//health_divisor))-1)*' '+'|',
        5: '',
        6: "     GOLD",
        7: "    " + seventh_line,
        8: "    Hero #" + str(hero_number)
        }
    
    for i in range(len(board)//size):
        out_board += board[i*size:(i+1)*size]
        if i < 9:
            out_board += meta_data[i]
        out_board += '\n'
        
    return(out_board + '\n')

def get_new_game_state(session, server_url, key, mode='training', number_of_turns = 10):
    """Get a JSON from the server containing the current state of the game"""

    if(mode=='training'):
        #Don't pass the 'map' parameter if you want a random map
        params = { 'key': key, 'turns': number_of_turns, 'map': 'm1'}
        api_endpoint = '/api/training'
    elif(mode=='arena'):
        params = { 'key': key}
        api_endpoint = '/api/arena'

    #Wait for 10 minutes
    r = session.post(server_url + api_endpoint, params, timeout=10*60)

    if(r.status_code == 200):
        print(return_board(r.json()))
        return r.json()
    else:
        print("Error when creating the game")
        print(r.text)

def move(session, url, direction):
    """Send a move to the server
    
    Moves can be one of: 'Stay', 'North', 'South', 'East', 'West' 
    """

    try:
        r = session.post(url, {'dir': direction}, timeout=TIMEOUT)

        if(r.status_code == 200):
            print(return_board(r.json()))
            return r.json()
        else:
            print("Error HTTP %d\n%s\n" % (r.status_code, r.text))
            return {'game': {'finished': True}}
    except requests.exceptions.RequestException as e:
        print(e)
        return {'game': {'finished': True}}


def is_finished(state):
    return state['game']['finished']

def start(server_url, key, mode, turns, bot):
    """Starts a game with all the required parameters"""

    # Create a requests session that will be used throughout the game
    session = requests.session()

    if(mode=='arena'):
        print(u'Connected and waiting for other players to join…')
    # Get the initial state
    state = get_new_game_state(session, server_url, key, mode, turns)
    print("Playing at: " + state['viewUrl'])

    while not is_finished(state):
        # Some nice output ;)
        sys.stdout.write('.')
        sys.stdout.flush()

        # Choose a move
        direction = bot.move(state)

        # Send the move and receive the updated game state
        url = state['playUrl']
        state = move(session, url, direction)

    # Clean up the session
    session.close()


if __name__ == "__main__":
    if (len(sys.argv) < 4):
        print("Usage: %s <key> <[training|arena]> <number-of-games|number-of-turns> [server-url]" % (sys.argv[0]))
        print('Example: %s mySecretKey training 20' % (sys.argv[0]))
    else:
        key = sys.argv[1]
        mode = sys.argv[2]

        if(mode == "training"):
            number_of_games = 1
            number_of_turns = int(sys.argv[3])
        else: 
            number_of_games = int(sys.argv[3])
            number_of_turns = 300 # Ignored in arena mode

        if(len(sys.argv) == 5):
            server_url = sys.argv[4]
        else:
            server_url = "http://vindinium.org"

        for i in range(number_of_games):
            start(server_url, key, mode, number_of_turns, Bot()) ## Here to change Bot
            print("\nGame finished: %d/%d" % (i+1, number_of_games))
