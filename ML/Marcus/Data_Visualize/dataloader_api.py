import os
import pandas as pd


def read_csv(csv_file):
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    csv_file = path + csv_file
    return pd.read_csv(csv_file)

def top_10_sale_game(dataframe, region='Global_Sales', genre=None, platform=None, year=0):
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
    sale = dataframe.head(10)[['Name', 'Platform', 'Developer', 'Critic_Score', region]]# modify it bt yourself
    return sale

def top_10_score_game(dataframe, genre=None, platform=None, year = 0):
    num_list = ['Critic_Score', 'User_Score', 'Year', 'Total_Shipped', 'Global_Sales', 'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales']
    for each in num_list:
        dataframe[each].fillna(0, inplace = True)
    dataframe['Global_Sales'] += dataframe['Total_Shipped'] #merge Total_Shipped and Global_Sales into Global_Sales
    useless_list = ['Total_Shipped'] #useless columns, modify by yourself
    dataframe.drop(columns = useless_list, inplace = True)
    dataframe.sort_values(by = ['Critic_Score'], ascending  = False, inplace = True)
    dataframe = dataframe[dataframe.Year > year]
    if genre:
        dataframe = dataframe[dataframe['Genre'].str.contains(genre)]
    if platform:
        dataframe = dataframe[dataframe['Platform'].str.contains(platform)]
    score = dataframe.head(10)[['Name', 'Platform', 'Critic_Score']]# modify it bt yourself
    return score

def game_count_yearly(dataframe, year = None, platform = None, genre = None): # from 1990~2018
    dataframe = dataframe[dataframe.Year >= 1990]
    dataframe = dataframe[dataframe.Year <= 2018]
    if genre:
        dataframe = dataframe[dataframe.Genre == genre]
    if year:
        dataframe = dataframe[dataframe.Year >= year]#show counts every year
        #dataframe = dataframe[dataframe.Year == year] show counts one year
    if platform:
        dataframe = dataframe[dataframe.Platform == platform]
    dataframe = dataframe.groupby(['Genre', 'Year']).size().reset_index(name='counts')
    return dataframe

def top_10_sale_genre(dataframe, year = None, platform = None): # top 9 genre + rest(other)
    dataframe['Global_Sales'].fillna(0, inplace = True)
    if year:
        dataframe = dataframe[dataframe.Year >= year]
    if platform:
        dataframe = dataframe[dataframe.Platform == platform]
    dataframe = dataframe.groupby(['Genre', 'Year', 'Platform', 'Global_Sales']).size().reset_index(name='counts')
    dataframe = dataframe.groupby(['Genre'])['Genre','Global_Sales'].sum()
    col_name = dataframe.columns.tolist()[0]
    col_list = dataframe.sort_values(by = col_name, ascending  = False).head(9).index.tolist()
    for each in dataframe.index:
        if each not in col_list:
            dataframe.rename(index={each: 'other'}, inplace = True)
    dataframe = pd.DataFrame(dataframe.groupby([dataframe.index])[col_name].sum())
    return dataframe

def top_10_count_genre(dataframe, year = None, platform = None): # top 9 genre + rest(other)
    dataframe['Global_Sales'].fillna(0, inplace = True)
    if year:
        dataframe = dataframe[dataframe.Year >= year]
    if platform:
        dataframe = dataframe[dataframe.Platform == platform]
    dataframe = dataframe.groupby(['Genre', 'Year', 'Platform']).size().reset_index(name='counts')
    dataframe = dataframe.groupby(['Genre'])['Genre','counts'].sum()
    col_name = dataframe.columns.tolist()[0]
    col_list = dataframe.sort_values(by = col_name, ascending  = False).head(9).index.tolist()
    for each in dataframe.index:
        if each not in col_list:
            dataframe.rename(index={each: 'other'}, inplace = True)
    dataframe = pd.DataFrame(dataframe.groupby([dataframe.index])[col_name].sum())
    return dataframe

def average_score(dataframe, genre, platform):
    dataframe.dropna(subset=['Critic_Score'], inplace = True)
    dataframe = dataframe[dataframe.Platform == platform]
    dataframe = dataframe[dataframe.Genre == genre]
    dataframe = dataframe[dataframe.Critic_Score > 0]
    average_score = dataframe['Critic_Score'].mean()
    return average_score

def average_sale(dataframe, genre, platform):
    dataframe.dropna(subset=['Global_Sales'], inplace = True)
    dataframe = dataframe[dataframe.Platform == platform]
    dataframe = dataframe[dataframe.Genre == genre]
    dataframe = dataframe[dataframe.Global_Sales > 0]
    average_sale = dataframe['Global_Sales'].mean()
    return average_sale

if __name__ == '__main__':
    full_file = r'\DataSet\vgsales-12-4-2019.csv'
    df_full = read_csv(full_file)

    #fun1: display top 10 sales, 
    #can modify 4 parameter:region, genre, platform, year
    #will show 'Name', 'Platform', 'Developer', 'Critic_Score', region_sale
    test = top_10_sale_game(df_full, year = 2016)
    #print(test)

    #fun2: display top 10 score, 
    #can modify 3 parameter:genre, platform, year
    #will show 'Name', 'Platform', 'Critic_Score'
    test = top_10_score_game(df_full, year = 2016)
    #print(test)

    #fun3: display the number of games yearly based on year and genre
    #can modify 3 parameter:region, genre, platform, year
    #will show 'Genre', 'Year', counts
    test = game_count_yearly(df_full, year = 2006, genre = 'Action')
    #print(test)

    #fun4: display top 9 sales genre + rest(other)
    #can modify 2 parameter:platform, year
    #will show 'Genre', sale
    test = top_10_sale_genre(df_full, year = 2014, platform = 'PS4')
    #print(test)

    #fun4: display top 9 count genre + rest(other)
    #can modify 2 parameter:platform, year
    #will show 'Genre', coutns
    test = top_10_count_genre(df_full, year = 2014, platform = 'PS4')
    #print(test)

    #fun5: display average score
    #2 parameter: genre & platform
    #will return a value
    test = average_score(df_full, genre = 'Action', platform = 'PS3')
    #print(test)

    #fun6: display average sale
    #2 parameter: genre & platform
    #will return a value
    test = average_sale(df_full, genre = 'Action', platform = 'PC')
    #print(test)