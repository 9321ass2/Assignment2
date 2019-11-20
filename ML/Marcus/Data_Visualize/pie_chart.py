from dataloader import *
import os
import matplotlib.pyplot as plt
import pandas as pd

def pre_process_pie(dataframe, year = None, platform = None, s_or_c = 0): # s_or_c == 0, counts ; s_or_c == 1, sales!!!!!
    dataframe['Global_Sales'].fillna(0, inplace = True)
    if year:
        dataframe = dataframe[dataframe.Year >= year]
    if platform:
        dataframe = dataframe[dataframe.Platform == platform]
    if not s_or_c:
        dataframe = dataframe.groupby(['Genre', 'Year', 'Platform']).size().reset_index(name='counts')
        dataframe = dataframe.groupby(['Genre'])['Genre','counts'].sum()
    else:
        dataframe = dataframe.groupby(['Genre', 'Year', 'Platform', 'Global_Sales']).size().reset_index(name='counts')
        dataframe = dataframe.groupby(['Genre'])['Genre','Global_Sales'].sum()
    col_name = dataframe.columns.tolist()[0]
    col_list = dataframe.sort_values(by = col_name, ascending  = False).head(9).index.tolist()
    for each in dataframe.index:
        if each not in col_list:
            dataframe.rename(index={each: 'other'}, inplace = True)
    dataframe = pd.DataFrame(dataframe.groupby([dataframe.index])[col_name].sum())
    return dataframe

def display_pie(df, s_or_c = 0):
    plt.figure(figsize=(7,7))#figure size
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
    title = 'Sales' if s_or_c else 'Counts'
    plt.title(f'{title} proportion',fontsize='large')
    #plt.show()



if __name__ == '__main__':
    full_file = r'\DataSet\vgsales-12-4-2019.csv'
    df_full = read_csv(full_file)
    # s_or_c == 0, counts ; s_or_c == 1, sales
    df_sales = pre_process_pie(df_full, platform = 'PS4', s_or_c = 1)#sales
    display_pie(df_sales, s_or_c = 1)
    df_count = pre_process_pie(df_full, platform = 'PS4', s_or_c = 0)#counts
    display_pie(df_count,  s_or_c = 0)
    plt.show()