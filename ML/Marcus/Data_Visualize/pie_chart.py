from dataloader import *
import os
import matplotlib.pyplot as plt
import pandas as pd

def pre_process_pie(dataframe, year = None, platform = None, genre = None, s_or_c = 0): # s_or_c == 0, counts ; s_or_c == 1, sales
    dataframe['Global_Sales'].fillna(0, inplace = True)
    #total_count = dataframe.groupby(['Year', 'Platform'])['counts'].sum()
    #dataframe = pd.merge(dataframe, total_count, on='Year')
    #dataframe.rename({'counts_x': 'counts', 'counts_y': 'total_counts'}, axis=1, inplace=True)
    if year:
        dataframe = dataframe[dataframe.Year >= year]
    if platform:
        dataframe = dataframe[dataframe.Platform == platform]
    if genre:
        dataframe = dataframe[dataframe.Genre == genre]
    if not s_or_c:
        dataframe = dataframe.groupby(['Genre', 'Year', 'Platform']).size().reset_index(name='counts')
        dataframe = dataframe.groupby(['Genre'])['Genre','counts'].sum()
    else:
        dataframe = dataframe.groupby(['Genre', 'Year', 'Platform', 'Global_Sales']).size().reset_index(name='counts')
        dataframe = dataframe.groupby(['Genre'])['Genre','Global_Sales'].sum()
    return dataframe

def display_pie(df):
    plt.figure(figsize=(10,10))
    df_column = df.columns.tolist()
    sizes = df[df_column[0]]
    labels = df.index
    explode = tuple([0 for _ in range(len(sizes.tolist()))])
    patches,text1,text2 = plt.pie(sizes,
                          explode = explode,
                          labels= labels,
                          autopct = '%3.2f%%',
                          shadow = False, 
                          startangle =90, 
                          pctdistance = 0.5)
    #plt.show()



if __name__ == '__main__':
    full_file = r'\DataSet\vgsales-12-4-2019.csv'
    df_full = read_csv(full_file)
    # s_or_c == 0, counts ; s_or_c == 1, sales
    df_count = pre_process_pie(df_full, platform = 'PS4', s_or_c = 1)#sales
    display_pie(df_count)
    df_sale = pre_process_pie(df_full, platform = 'PS4', s_or_c = 0)#counts
    display_pie(df_sale)
    plt.show()