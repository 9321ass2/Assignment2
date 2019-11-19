import os
import pandas as pd


def read_csv(csv_file):
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    csv_file = path + csv_file
    return pd.read_csv(csv_file)

def pre_process_top(dataframe, region=None, genere=None, platform=None, s_or_r = 0):
    dataframe.loc[dataframe['Global_Sales'].isnull(),'Global_Sales'] = dataframe[dataframe['Global_Sales'].isnull()]['Total_Shipped']
    label = 'Platform'
    if platform:
        dataframe = dataframe[dataframe['Platform'].str.contains(platform)]
        label = 'Genre'
    if genere:
        dataframe = dataframe[dataframe['Genre'].str.contains(genere)]
    if s_or_r:
        sale = dataframe.sort_values(by = ['Global_Sales'], ascending  = False)
        sale = sale.head(10)[['Name', label, 'Global_Sales']]
        print(sale)
        return sale
    else:
        dataframe.sort_values(by = ['Critic_Score'], ascending = False, inplace = True)
        sale = dataframe.head(10)[['Name', 'Platform', 'Critic_Score']]

def pre_process_LR(dataframe, region = None, genere = None, platform = None):
    dataframe.dropna(how = 'all', subset=['Global_Sales', 'Total_Shipped'], inplace = True) #clean total sale is Null
    dataframe.dropna(subset = ['Year'], inplace = True) #clean year is Null
    dataframe.loc[dataframe['Global_Sales'].isnull(),'Global_Sales'] = dataframe[dataframe['Global_Sales'].isnull()]['Total_Shipped'] #merge Total_Shipped and Global_Sales into Global_Sales
    dataframe = dataframe.drop(dataframe[(dataframe.Other_Sales > 100)].index) #clean Other_Sales is year, e.g. the sale is 2007
    sale_list = ['NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales'] # fill null sale with 0
    for each in sale_list:
        dataframe[each].fillna(0, inplace = True)
    useless_list = ['Rank', 'ESRB_Rating', 'Publisher', 'Developer', 'Critic_Score', 'User_Score', 'Total_Shipped'] #useless columns, modify by yourself
    dataframe.drop(columns = useless_list, inplace = True)
    if platform:
        dataframe = dataframe[dataframe['Platform'].str.contains(platform)] # filter platform
    if genere:
        dataframe = dataframe[dataframe['Genre'].str.contains(genere)] # filter genre
    if region:
        sale_list.append('Global_Sales')
        sale_list.remove(region)
        dataframe.drop(columns = sale_list, inplace = True) # drop unnecessary sales, keep regional sales
    else:
        dataframe.drop(columns = sale_list, inplace = True) # only keep global sales
    return dataframe

def pre_process_LR_count(dataframe): # for RL counts -> genre
    dataframe = dataframe.groupby(['Genre', 'Year']).size().reset_index(name='counts')
    total_count = dataframe.groupby(['Year'])['counts'].sum()
    dataframe = pd.merge(dataframe, total_count, on='Year')
    dataframe.rename({'counts_x': 'counts', 'counts_y': 'total_counts'}, axis=1, inplace=True)
    return dataframe

def pre_process_LR_sale(dataframe):
    dataframe['rate'] = dataframe.Global_Sales / (2020 - dataframe.Year)
    for i in range(int(max(dataframe.Year))-1, int(min(dataframe.Year))-1, -1):
        sale = dataframe.Global_Sales - (2020 - i) * dataframe.rate
        temp = []
        for each in sale.values:
             temp.append(each if each > 0 else 0)
        dataframe[str(i)] = temp
    return dataframe

    # dataframe.to_csv('sale.csv', index = False)


def pre_process_KNN(dataframe, region = None, genere = None, platform = None):
    num_list = ['Critic_Score', 'User_Score', 'Year', 'Total_Shipped', 'Global_Sales', 'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales']
    string_list = ['Genre', 'ESRB_Rating', 'Platform', 'Publisher', 'Developer']
    for each in num_list:
        dataframe[each].fillna(0, inplace = True)
    for each in string_list:
        dataframe[each].fillna('Unknown', inplace = True)
    dataframe = dataframe.drop(dataframe[(dataframe.Other_Sales > 100)].index) #clean Other_Sales is year, e.g. the sale is 2007
    dataframe['Global_Sales'] += dataframe['Total_Shipped'] #merge Total_Shipped and Global_Sales into Global_Sales
    useless_list = ['Total_Shipped'] #useless columns, modify by yourself
    dataframe.drop(columns = useless_list, inplace = True)

    # some filters, if you need
    # if platform:
    #     dataframe = dataframe[dataframe['Platform'].str.contains(platform)] # filter platform
    # if genere:
    #     dataframe = dataframe[dataframe['Genre'].str.contains(genere)] # filter genre
    # if region:
    #     sale_list.append('Global_Sales')
    #     sale_list.remove(region)
    #     dataframe.drop(columns = sale_list, inplace = True) # drop unnecessary sales, keep regional sales
    # else:
    #     dataframe.drop(columns = sale_list, inplace = True) # only keep global sales

    #dataframe.to_csv('KNN.csv', index = False)
    return dataframe

def game_30(df_pop, df_full):
    df_pop.columns = ['Rank']
    temp = pd.DataFrame([[1]], columns=['Rank'])
    df_pop = pd.concat([temp, df_pop], sort=False)
    pop_30 = pd.merge(df_pop, df_full, on='Rank')
    return pop_30

if __name__ == '__main__':
    csv_file = r'\DataSet\vgsales-12-4-2019-short.csv'
    full_file = r'\DataSet\vgsales-12-4-2019.csv'
    pop_file = r'\DataSet\popular_games_output.csv'

    df = read_csv(csv_file)
    df_full = read_csv(full_file)
    df_pop = read_csv(pop_file)

    #game_30(df_pop, df_full)

    # processed_df = pre_process_top(df, s_or_r = 1)
    # processed_df = pre_process_top(df, platform = 'PC', s_or_r = 1)
    #df = pre_process_KNN(df)

    #df = pre_process_LR_sale(df)
    #df = pre_process_LR_count(df)