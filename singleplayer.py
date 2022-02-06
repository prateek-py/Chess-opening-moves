from func import*
import pandas as pd

def get_player_opening_data(username,game='blitz',mingames=100):
    '''gives the opening moves count for a player'''

    game_data_list=get_min_games(username, game, mingames)

    dicW = {}
    dicB = {}
    count=0
    for i in range(len(game_data_list)):

        try:
            move=get_opening_move(game_data_list[i],username)

        except:
            pass
        else:
            if move!=None:
                if get_color(game_data_list[i],username)=='W':
                    dicW[move]= dicW.setdefault(move, 0)+1
                else:
                    dicB[move]= dicB.setdefault(move, 0)+1

    dfW=(pd.DataFrame.from_dict(dicW,orient='index', columns=['count'])).sort_values(by=['count'], ascending=False)
    dfB=(pd.DataFrame.from_dict(dicB,orient='index', columns=['count'])).sort_values(by=['count'], ascending=False)
    return dfW,dfB



