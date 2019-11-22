# This file is to generate 30 games which are most popular in history.
# The final output is a csv file which contains the 'Rank' of the 30 games.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import sys, os

# Function 'game_30' is written by Marcus !!!
def game_30(df_pop, df_full):
    df_pop.columns = ['Rank']
    temp = pd.DataFrame([[1]], columns=['Rank'])
    df_pop = pd.concat([temp, df_pop], sort=False)
    pop_30 = pd.merge(df_pop, df_full, on='Rank')
    return pop_30


if __name__ == "__main__":
    origin_file = pd.read_csv('../ML/DataSet/vgsales-12-4-2019-short.csv').head(3000)
    useless_columns = ['Publisher', 'Developer',
                       'Critic_Score', 'User_Score', 'Total_Shipped', 'Global_Sales', 
                       'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales']
    origin_file = origin_file.drop(columns=useless_columns).dropna()
    most_popular = set({})
    rank = 1
    # To cover all kinds of games, we need to find out how many 'Genre' of games exist in the dataset. 
    Genre = list(set(origin_file['Genre']))  # Turned out to be 17.
    # Also, we need to cover all kinds of ESRB_Ratings.
    ESRB = list(set(origin_file['ESRB_Rating'].dropna()))  # Turned out to be 5.
    Genre_17 = set({})
    ESRB_5 = set({})
    lonely_game = []
    for game in origin_file.itertuples():
        temp = origin_file[origin_file['Genre'] == game[3]]
        if temp.shape[0] == 1:
            lonely_game.append(game[1])
            continue
        if game[3] not in Genre_17:
            Genre_17.add(game[3])
            most_popular.add(game[1])
        if game[4] not in ESRB_5:
            ESRB_5.add(game[4])
            most_popular.add(game[1])
        if len(Genre_17) == 17 and len(ESRB_5) == 5:
            break
    for i in range(1, 200):
        if i in lonely_game:
            continue
        else:
            most_popular.add(i)
            if len(most_popular) == 30:
                break
    most_popular = sorted(list(most_popular))
    pd.DataFrame(most_popular).to_csv(
        '../ML/DataSet/popular_games_output.csv', index=False, header=False)
    mp = pd.read_csv('../ML/DataSet/popular_games_output.csv')
    full = pd.read_csv('../ML/Data_Visualize/KNN.csv')
    game_30(mp, full).to_csv('../ML/DataSet/game_30.csv', index=False)
    print('Success')
    
