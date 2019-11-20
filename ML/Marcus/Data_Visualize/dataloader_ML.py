import os
import pandas as pd


def read_csv(csv_file):
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    csv_file = path + csv_file
    return pd.read_csv(csv_file)

def pre_process_top(dataframe, region='Global_Sales', genere=None, platform=None, year=0):
    num_list = ['Critic_Score', 'User_Score', 'Year', 'Total_Shipped', 'Global_Sales', 'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales']
    for each in num_list:
        dataframe[each].fillna(0, inplace = True)
    dataframe['Global_Sales'] += dataframe['Total_Shipped'] #merge Total_Shipped and Global_Sales into Global_Sales
    dataframe.sort_values(by = [region], ascending  = False, inplace = True)
    dataframe = dataframe[dataframe.Year > year]
    if genere:
        dataframe = dataframe[dataframe['Genre'].str.contains(genere)]
    if platform:
        dataframe = dataframe[dataframe['Platform'].str.contains(platform)]
    sale = dataframe.head(10)[['Name', 'Platform', 'Developer', 'Critic_Score', region]]
    print(sale)
    return sale

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

def pre_process_LR_ESRN_NULL(dataframe):
    num_list = ['Total_Shipped', 'Global_Sales' ]
    for each in num_list:
        dataframe[each].fillna(0, inplace = True)
    dataframe['Total_Shipped'] += dataframe['Global_Sales']
    useless_list = ['VGChartz_Score', 'Critic_Score', 'User_Score', 'Global_Sales', 'NA_Sales', 'PAL_Sales', 'JP_Sales' ,'Other_Sales' ,'Year' ,'Last_Update' ,'url' ,'status' ,'Vgchartzscore' ,'img_url']
    dataframe.drop(columns = useless_list, inplace = True)
    df_NOT_NULL = dataframe.dropna(subset=['ESRB_Rating'])
    df_NULL = dataframe[dataframe['ESRB_Rating'].isnull()]
    df_NOT_NULL.to_csv('df_NOT_NULL.csv', index = False)
    df_NULL.to_csv('df_NULL.csv', index = False)
    useless_list.append('ESRB_Rating')
    dataframe.drop(columns = useless_list, inplace = True)
    dataframe.to_csv('df_ALL.csv', index = False)
    return dataframe

    # dataframe.to_csv('sale.csv', index = False)

def pre_process_LR_0_2020(dataframe):
    useless_list = ['VGChartz_Score', 'Critic_Score', 'User_Score', 'Total_Shipped', 'Global_Sales', 'NA_Sales', 'PAL_Sales', 'JP_Sales' ,'Other_Sales' ,'Last_Update' ,'url' ,'status' ,'Vgchartzscore' ,'img_url']
    dataframe.drop(columns = useless_list, inplace = True)
    dataframe['Year'].fillna(0, inplace = True)
    df_0 = dataframe[dataframe['Year'] == 0]
    df_2020 = dataframe[dataframe['Year'] == 2020]
    frames = [df_0, df_2020]
    df_0_2020 = pd.concat(frames)

    dataframe.drop(dataframe[(dataframe.Year == 0) | (dataframe.Year == 2020)].index, inplace = True)
    df_0_2020.to_csv('df_0_2020.csv', index = False)
    dataframe.to_csv('df_other.csv', index = False)
    return dataframe

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
    pop_30.to_csv('game_30.csv', index = False)
    return pop_30

def somne_useful_list(dataframe, column_name):
    column = [column_name]
    result = dataframe.drop_duplicates(subset=column)[column_name]
    result.to_csv(f'{column_name}.csv', index = False, header=False)
    return result

def sale_region(df_sale, df_region):
    num_list = ['Critic_Score', 'User_Score', 'Year', 'Total_Shipped', 'Global_Sales', 'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales']
    for each in num_list:
        df_sale[each].fillna(0, inplace = True)
    df_sale = df_sale[['NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales']].sum()
    '''
    NA_Sales       3572.12    0
    PAL_Sales      2047.76    1
    JP_Sales        777.56    2
    Other_Sales     694.13    3
    '''
    df_janpan = df_region[df_region.Country == 'Japan '][['Country', 'Region', 'Population']]
    region = ['EUROPE', 'NORTHERN AMERICA']
    df_region.replace({'EASTERN EUROPE                     ':'EUROPE'}, inplace = True)
    df_region.replace({'WESTERN EUROPE                     ':'EUROPE'}, inplace = True)
    df_region.replace({'NORTHERN AMERICA                   ':'NORTHERN AMERICA'}, inplace = True)
    df_region = df_region[df_region['Region'].isin(region)][['Country', 'Region', 'Population']]
    df_region = pd.concat([df_region, df_janpan])
    region.append('ASIA (EX. NEAR EAST)         ')
    person = df_region.groupby(['Region']).sum()
    region_dict = {}
    person_dict = {}
    '''
                               Population
Region                                   
ASIA (EX. NEAR EAST)            127463611
EUROPE                          516254715
NORTHERN AMERICA                331672307
    '''

    for each in region:
        if each == 'EUROPE':
            region_dict[each] = df_sale[1]
            person_dict[each] = person['Population'][1]
        elif each == 'NORTHERN AMERICA':
            region_dict[each] = df_sale[0]
            person_dict[each] = person['Population'][2]
        else:
            region_dict[each] = df_sale[2]
            person_dict[each] = person['Population'][0]
    df_region['region_sale'] = df_region.Region.apply(lambda x: region_dict[x])
    df_region['region_population'] = df_region.Region.apply(lambda x: person_dict[x])
    df_region['region_per_person'] = df_region['region_sale']/df_region['region_population'] * 1000000
    df_region['country_sale'] = df_region['region_per_person'] * df_region['Population'] 
    df_region.to_csv('sale_country.csv')
    print(df_region)
    return df_region




if __name__ == '__main__':
    csv_file = r'\DataSet\vgsales-12-4-2019-short.csv'
    full_file = r'\DataSet\vgsales-12-4-2019.csv'
    pop_file = r'\DataSet\popular_games_output.csv'
    knn_file = r'\DataSet\KNN.csv'
    region_file = r'\DataSet\countries of the world.csv'
    #df = read_csv(csv_file)
    df_full = read_csv(full_file)
    #pre_process_top(df_full, year = 2016)
    #pre_process_LR_ESRN_NULL(df_full)
    #pre_process_LR_0_2020(df_full)
    #df_pop = read_csv(pop_file)
    #df_KNN = pre_process_KNN(df_full)
    #game_30(df_pop, df_KNN)

    # processed_df = pre_process_top(df, s_or_r = 1)
    # processed_df = pre_process_top(df, platform = 'PC', s_or_r = 1)

    #df = pre_process_LR_sale(df)
    #df = pre_process_LR_count(df)
    # column_name = 'Genre'
    # somne_useful_list(df_full, column_name)
    # column_name = 'Platform'
    # somne_useful_list(df_full, column_name)
    # column_name = 'Publisher'
    # somne_useful_list(df_full, column_name)
    df_region = read_csv(region_file)
    sale_region(df_full, df_region)