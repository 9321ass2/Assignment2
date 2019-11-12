# This file is to generate 30 games which are most popular in history.
# The final output is a csv file which contains the 'Rank' of the 30 games.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import sys, os


if __name__ == "__main__":
    origin_file = pd.read_csv('./DataSet/vgsales-12-4-2019-short.csv')
    copy = origin_file
    useless_columns = ['Publisher', 'Developer',
                       'Critic_Score', 'User_Score', 'Total_Shipped', 'Global_Sales', 
                       'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales']
    origin_file = origin_file.drop(columns=useless_columns).dropna()
    most_popular = list(np.arange(1, 21))
    rank = 1
    # To cover all kinds of games, we need to find out how many 'Genre' of games exist in the dataset. 
    Genre = list(set(origin_file['Genre']))  # Turned out to be 20.
    # Also, we need to cover all kinds of ESRB_Ratings.
    ESRB = list(set(origin_file['ESRB_Rating'].dropna()))  # Turned out to be 8.
    Genre_20 = []
    ESRB_8 = []
    for game in origin_file.itertuples():
        if game[3] not in Genre_20:
            Genre_20.append(game[3])
            most_popular.append(game[1])
        if game[4] not in ESRB_8:
            ESRB_8.append(game[4])
            most_popular.append(game[1])
        most_popular = list(set(most_popular))
        if len(most_popular) == 30:
            break
    pd.DataFrame(sorted(most_popular)).to_csv(
        './DataSet/popular_games_output.csv', index=False, header=False)
