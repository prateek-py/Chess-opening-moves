import urllib.request, urllib.parse, urllib.error
import json
import re


def get_api_data(url):
    '''takes url and returns data collected'''
    try:
        uh = urllib.request.urlopen(url)
        data = uh.read().decode()
        js = json.loads(data)
        return js
    except:
        raise Exception("Sorry, no such username available")

def get_leaderboard_data():
    '''fetches the leaderboard data'''
    url='https://api.chess.com/pub/leaderboards'
    data= get_api_data(url)
    return data

def get_min_games(username, gformat, mingames=100):
    '''get min game data for a given username in a particular game format.
         gformat can be 'blitz', 'bullet', 'rapid'
         Default games = 100
         mingames doesn't specify the exact number but just a minimum due to the 
         way data is received via the api'''
    
    url = f'https://api.chess.com/pub/player/{username}/games/archives'
    apidata= get_api_data(url)
    game_data=[]
    k=1
    try:
        while len(game_data)<mingames:
            arch_games=apidata['archives'][-k]       #gives a list of urls for games played
            api_game= get_api_data(arch_games)
            for i in range(len(api_game['games'])):
                val=api_game['games'][i]
                if val['time_class']== gformat and val['rules']=='chess' and val['rated']==True:  # rules could be bughouse chess as well
                    game_data.append(val)
            k+=1
    except:
            pass
    return game_data


def get_pgn(game_data):
    '''fetches the pgn (only the move data) from the game data'''
    pgn=game_data['pgn'].split('\n')
    pgnformat1=pgn[22 if pgn[7][1:16]=='CurrentPosition' else 23]   # the tournament data and normal game data have a 1 line difference
    #now we will parse out the move data:
    pgnformat2 = re.sub(r"{.*?}",'',pgnformat1)
    pgnformat3 = re.sub(r"{.*?}",'',pgnformat2)
    final_pgn= re.sub(r"\s\d*\.\.\.",'',pgnformat3)
    return final_pgn

def get_opening_move(game_data,username):
    '''gives the opening move of the game played by the username'''      
    if game_data['pgn'].split('\n')[4].split('"')[1]==username:
        return get_pgn(game_data).split()[1]    #username is white
    else:
        ret=get_pgn(game_data).split()[2]       #username is black
        return ret if ret!='1-0' and ret!='0-1' else None   #if username resigns after 1st move

def get_color(game_data,username):
    '''if the player is black or white'''
      
    if game_data['pgn'].split('\n')[4].split('"')[1]==username:
        return 'W'
    else:
        return 'B'
