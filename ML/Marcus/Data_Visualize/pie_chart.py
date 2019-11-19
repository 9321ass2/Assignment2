from dataloader import *
import os
import matplotlib.pyplot as plt
import pandas as pd

def pie_preprocess(df, year = None):
    if year:
        df = df[df.Year >= year]
    df = df.groupby(['Genre'])['Genre','counts'].sum()
    return df

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
    df_count = pre_process_LR_count(df_full)
    df_count = pie_preprocess(df_count, year = None)
    display_pie(df_count)