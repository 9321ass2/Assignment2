import os
import matplotlib.pyplot as plt
import pandas as pd


def read_csv(csv_file):
    return pd.read_csv(csv_file)

def pre_process(dataframe, region='Global_Sales', genere=None, platform=None, s_or_r = 0):
    num_list = ['Critic_Score', 'User_Score', 'Year', 'Total_Shipped', 'Global_Sales', 'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales']
    for each in num_list:
        dataframe[each].fillna(0, inplace = True)
    dataframe['Global_Sales'] += dataframe['Total_Shipped'] #merge Total_Shipped and Global_Sales into Global_Sales
    useless_list = ['Total_Shipped'] #useless columns, modify by yourself
    dataframe.drop(columns = useless_list, inplace = True)
    if s_or_r:
        dataframe.sort_values(by = [region], ascending  = False, inplace = True)
        if genere:
            dataframe = dataframe[dataframe['Genre'].str.contains(genere)]
            sale = dataframe.head(10)[['Name', 'Platform', region]]
        if platform:
            dataframe = dataframe[dataframe['Platform'].str.contains(platform)]
            sale = dataframe.head(10)[['Name', 'Genre', region]]
        if genere and platform:
            sale = dataframe.head(10)[['Name', region]]
        sale = dataframe.head(10)[['Name', region]]
        return sale
    else:
        dataframe.sort_values(by = ['Critic_Score'], ascending  = False, inplace = True)
        sale = dataframe.head(10)[['Name', 'Platform', 'Critic_Score']]
        print(sale)

def display_chart(dataframe):
    dataframe.sort_values(by = dataframe.columns[-1], ascending  = True, inplace = True)
    x = dataframe[dataframe.columns[-1]]
    y = dataframe[dataframe.columns[0]]
    plt.barh(y,x, height = 0.5)
    plt.title('Top Sales Games for All Platforms')
    plt.yticks(fontsize=5)
    plt.show()


if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    csv_file = r'\DataSet\vgsales-12-4-2019-short.csv'
    csv_file = path + csv_file
    df = read_csv(csv_file)
    #processed_df = pre_process(df, s_or_r = 1, genere = 'Action')
    #processed_df = pre_process(df, s_or_r = 1, platform = 'PC')
    processed_df = pre_process(df, s_or_r = 1, genere = 'Action', platform = 'PC')
    #processed_df = pre_process(df, s_or_r = 1)
    display_chart(processed_df)

