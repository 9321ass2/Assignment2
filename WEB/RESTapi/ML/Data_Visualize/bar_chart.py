import os
import matplotlib.pyplot as plt
import pandas as pd


def read_csv(csv_file):
    return pd.read_csv(csv_file)

def pre_process(dataframe, region='Global_Sales', genere='all', platform='all', s_or_r = 0):
    if s_or_r:
        dataframe.sort_values(by = ['Global_Sales'], ascending  = False, inplace = True)
        sale = dataframe.head(10)[['Name', 'Platform', region]]
        return sale
    else:
        dataframe.sort_values(by = ['Critic_Score'], ascending  = False, inplace = True)
        sale = dataframe.head(10)[['Name', 'Platform', 'Critic_Score']]
        print(sale)

def display_chart(dataframe):
    dataframe.sort_values(by = ['Global_Sales'], ascending  = True, inplace = True)
    x = dataframe['Global_Sales']
    y = dataframe['Name']
    print(dataframe)
    plt.barh(dataframe['Name'], dataframe['Global_Sales'], height = 0.5)
    plt.title('Top Sales Games for All Platforms')
    plt.yticks(fontsize=5)
    plt.show()


if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    csv_file = r'\DataSet\vgsales-12-4-2019-short.csv'
    csv_file = path + csv_file
    df = read_csv(csv_file)
    processed_df = pre_process(df, s_or_r = 1)
    display_chart(processed_df)

