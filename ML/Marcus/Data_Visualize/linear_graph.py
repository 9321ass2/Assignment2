from dataloader import *
import os
import matplotlib.pyplot as plt
import pandas as pd

def pre_process_linear(dataframe, year = None, platform = None): # from 1990~2018
    dataframe = dataframe[dataframe.Year >= 1990]
    dataframe = dataframe[dataframe.Year <= 2018]
    if year:
        dataframe = dataframe[dataframe.Year >= year]
    if platform:
        dataframe = dataframe[dataframe.Platform == platform]
    dataframe = dataframe.groupby(['Genre', 'Year']).size().reset_index(name='counts')
    return dataframe

def display_linear(dataframe, genre_1, genre_2 = None): #genre2 is optional
    df_g1 = dataframe[dataframe.Genre == genre_1][['Year', 'counts']]
    year = df_g1['Year'].tolist()
    count_1 = df_g1['counts'].tolist()
    plt.plot(year,count_1,"x-",label=genre_1)
    if genre_2:
        df_g2 = dataframe[dataframe.Genre == genre_2][['Year', 'counts']]
        count_2 = df_g2['counts'].tolist()
        plt.plot(year,count_2,"+-",label=genre_2)
    plt.xlabel('Year')
    plt.ylabel('Number of Games')
    plt.grid(True)
    plt.legend(loc=2, borderaxespad=1)
    plt.show()

if __name__ == '__main__':
    full_file = r'\DataSet\vgsales-12-4-2019.csv'
    df_full = read_csv(full_file)
    # s_or_c == 0, counts ; s_or_c == 1, sales
    df_linear = pre_process_linear(df_full)# can modify year and platform
    display_linear(df_linear, genre_1 = 'Action', genre_2 = 'Misc') # genre2 is optional