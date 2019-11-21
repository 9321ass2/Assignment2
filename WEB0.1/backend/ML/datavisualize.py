import pandas as pd
import json
from infra.function import *
def pre_process_top(dataframe, region='Global_Sales', genere=None, platform=None, year=0):
    num_list = ['Critic_Score', 'User_Score', 'Year', 'Total_Shipped', 'Global_Sales', 'NA_Sales', 'PAL_Sales',
                'JP_Sales', 'Other_Sales']
    for each in num_list:
        dataframe[each].fillna(0, inplace=True)
    dataframe['Global_Sales'] += dataframe['Total_Shipped']  # merge Total_Shipped and Global_Sales into Global_Sales
    dataframe.sort_values(by=[region], ascending=False, inplace=True)
    dataframe = dataframe[dataframe.Year > year]
    if genere:
        dataframe = dataframe[dataframe['Genre'].str.contains(genere)]
    if platform:
        dataframe = dataframe[dataframe['Platform'].str.contains(platform)]
    sale = dataframe.head(10)[['Name', 'Platform', 'Developer', 'Critic_Score', region]]
    return sale


def Create_Top3Sales():
    full_file = "./ML/DataSet/vgsales-12-4-2019.csv"
    df_full = pd.read_csv(full_file)
    df_topsales = pre_process_top(df_full, year=2016).head(3)
    top3list = []
    for x in df_topsales.Name:
        top3list.append([x])
    i = 0
    for x in df_topsales.Platform:
        top3list[i].append(x)
        i += 1
    i = 0
    for x in df_topsales.Developer:
        top3list[i].append(x)
        i += 1
    i = 0
    for x in df_topsales.Critic_Score:
        top3list[i].append(x)
        i += 1
    i = 0
    for x in df_topsales.Global_Sales:
        top3list[i].append(x)
        i += 1
    return top3list


def Create_Popular30(onlyID=False):
    csv_file = "./ML/DataSet/game_30.csv"
    df = pd.read_csv(csv_file)
    if onlyID:
        g30 = [int(element) for element in df['Rank']]
    else:
        g30 = df_to_json(df)
    return g30


def top_sale_game(top=10,region='Global_Sales', genre=None, platform=None, year=0):
    dataframe = pd.read_csv('./ML/DataSet/vgsales-12-4-2019.csv')
    num_list = ['Critic_Score', 'User_Score', 'Year', 'Total_Shipped', 'Global_Sales', 'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales']
    for each in num_list:
        dataframe[each].fillna(0, inplace = True)
    dataframe['Global_Sales'] += dataframe['Total_Shipped'] #merge Total_Shipped and Global_Sales into Global_Sales
    dataframe.sort_values(by = [region], ascending  = False, inplace = True)
    dataframe = dataframe[dataframe.Year > year]
    if genre:
        dataframe = dataframe[dataframe['Genre'].str.contains(genre)]
    if platform:
        dataframe = dataframe[dataframe['Platform'].str.contains(platform)]
    sale = dataframe.head(top)[['Name', 'Platform', 'Developer', 'Critic_Score', region]]# modify it bt yourself
    ret = df_to_json(sale)
    return ret

def top_score_game( genre=None, platform=None, year = 0):
    dataframe = pd.read_csv('./ML/DataSet/vgsales-12-4-2019.csv')
    num_list = ['Critic_Score', 'User_Score', 'Year', 'Total_Shipped', 'Global_Sales', 'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales']
    for each in num_list:
        dataframe[each].fillna(0, inplace = True)
    dataframe['Global_Sales'] += dataframe['Total_Shipped'] #merge Total_Shipped and Global_Sales into Global_Sales
    useless_list = ['Total_Shipped'] #useless columns, modify by yourself
    dataframe.drop(columns = useless_list, inplace = True)
    dataframe.sort_values(by = ['Critic_Score'], ascending  = False, inplace = True)
    score = dataframe.head(10)[['Name', 'Platform', 'Critic_Score']]# modify it bt yourself
    ret = df_to_json(score)
    return ret

full_file = './ML/DataSet/vgsales-12-4-2019.csv'
df_full = pd.read_csv(full_file)
Genre_list = list(dict.fromkeys(df_full['Genre']))
Platform_list = list(dict.fromkeys(df_full['Platform']))
Region_list = ['Global_Sales', 'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales']