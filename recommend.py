import numpy as np
import pandas as pd
import sys, os


# Input is a simple array with virable length.
# Array contains serval numbers refer to rank of games.
def get_user_favorite():
    uf = pd.read_csv('./Data_Visualize/user_favorite.csv')
    return uf

def get_all_games():
    ag = pd.read_csv('./Data_Visualize/KNN.csv')
    return ag

def get_pop_games():
    pg = pd.read_csv('./Data_Visualize/game_30.csv')
    return pg

def get_user_game_details(user_df, all_data):
    ESRB_list = []
    platform_list = []
    for i in user_df.itertuples():
        game_info = all_data[all_data['Rank'] == i[1]]
        ESRB_list.append(game_info['ESRB_Rating'].iloc[0])
        platform_list.append(game_info['Platform'].iloc[0])
        print(game_info['Name'].iloc[0])
    ESRB_list = list(set(ESRB_list))
    platform_list = list(set(platform_list))
    return ESRB_list, platform_list


def remove_useless_game(allgame, ESRB_list, platform_list):
    allgame = allgame[allgame['ESRB_Rating'].isin(ESRB_list)]
    allgame = allgame[allgame['Platform'].isin(platform_list)]
    return allgame


if __name__ == "__main__":
    usr_game = get_user_favorite()
    all_game = get_all_games()
    pop_game = get_pop_games()
    ESRB_list, platform_list = get_user_game_details(usr_game, all_game)
    useful_game = remove_useless_game(all_game, ESRB_list, platform_list) # The final dataframe to be used on knn
    # print(useful_game)
    
