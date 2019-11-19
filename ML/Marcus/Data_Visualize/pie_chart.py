from dataloader import *
import os
import matplotlib.pyplot as plt
import pandas as pd

def pre_process_count_pie(dataframe, year = None, platform = None, genre = None): # for RL counts -> genre
    dataframe = dataframe.groupby(['Genre', 'Year', 'Platform']).size().reset_index(name='counts')
    print(dataframe)
    #total_count = dataframe.groupby(['Year', 'Platform'])['counts'].sum()
    #dataframe = pd.merge(dataframe, total_count, on='Year')
    #dataframe.rename({'counts_x': 'counts', 'counts_y': 'total_counts'}, axis=1, inplace=True)
    print(dataframe)
    if year:
        dataframe = dataframe[dataframe.Year >= year]
    if 
    dataframe = dataframe.groupby(['Genre'])['Genre','counts'].sum()
    return dataframe

def display_pie(df):
    print(df)
    plt.figure(figsize=(10,10))
    sizes = df['counts']
    labels = df.index
    explode = tuple([0 for _ in range(len(sizes.tolist()))])
    patches,text1,text2 = plt.pie(sizes,
                          explode = explode,
                          labels= labels,
                          autopct = '%3.2f%%',
                          shadow = False, 
                          startangle =90, 
                          pctdistance = 0.5)
    plt.show()


if __name__ == '__main__':
    full_file = r'\DataSet\vgsales-12-4-2019.csv'
    df_full = read_csv(full_file)
    df_count = pre_process_count_pie(df_full)
    display_pie(df_count)