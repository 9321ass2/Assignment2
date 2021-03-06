import numpy as np
import pandas as pd


# Input is a simple array with variable length.
# Array contains serval numbers refer to rank of games.
def get_user_favorite():
    uf = [1, 9, 15, 3, 20, 283, 1617, 5, 20, 21]
    return uf


def get_all_games():
    ag = pd.read_csv('../Data_Visualize/KNN.csv')
    return ag


def get_pop_games():
    pg = pd.read_csv('../DataSet/game_30.csv')
    return pg


def get_ori_games():
    og = pd.read_csv('../DataSet/vgsales-12-4-2019.csv')
    return og


def get_user_game_details(user_df, all_data):
    ESRB_list = []
    platform_list = []
    for i in user_df:
        game_info = all_data[all_data['Rank'] == i]
        ESRB_list.append(game_info['ESRB_Rating'].iloc[0])
        platform_list.append(game_info['Platform'].iloc[0])
        # print(game_info['Name'].iloc[0])
    ESRB_list = list(set(ESRB_list))
    platform_list = list(set(platform_list))
    return ESRB_list, platform_list


def get_gram_matrix():
    df = pd.read_csv('../DataSet/relevance_matrix.csv')
    return df


if __name__ == "__main__":
    usr_game = get_user_favorite()
    all_game = get_all_games()
    pop_game = get_pop_games()
    get_url = get_ori_games()
    ESRB_list, platform_list = get_user_game_details(usr_game, all_game)
    gram_matrix = get_gram_matrix()
    recommend_list = []
    target_list = usr_game
    tar_num = len(target_list)
    for row in usr_game:
        matrix_column = row - 1
        cur_game_score = gram_matrix.iloc[matrix_column]
        cur_game_score = cur_game_score.sort_values(ascending=False)
        cur_game_recommend = []
        for rank in cur_game_score[1:].iteritems():
            if rank[1] == 0:
                break
            else:
                cur_game_recommend.append(rank)
        if len(cur_game_recommend) != 1:
            recommend_list.append(cur_game_recommend)
        # print(cur_game_recommend)
    final_list = []
    for i in recommend_list:
        step = 0
        for j in i:
            if j[1] != 1:
                final_list.append((int(j[0])+1, j[1]))
                step+=1
                if step>5:
                    break
    # print(final_list)
    final_list = pd.DataFrame(final_list)
    final_list = final_list.sort_values(by=[1], ascending=False)
    # print(final_list)
    output = []
    for row in final_list.itertuples():
        if (row[1] not in output) and (row[1] not in target_list):
            output.append(row[1])
    # print(output)
    output_df = pd.DataFrame(output).rename(
        columns={0: 'Rank'}).sort_values(by=['Rank'])
    game_name_list = []
    for i in output_df.itertuples():
        name = all_game[all_game['Rank'] == i[1]]['Name'].values[0]
        url = get_url[get_url['Rank'] == i[1]]['img_url'].values[0]
        if name not in game_name_list:
            output_df.loc[i[0], 'Name'] = name
            output_df.loc[i[0], 'img_url'] = url
            game_name_list.append(name)
        else:
            output_df.loc[i[0], 'Name'] = np.NaN
    output_df = output_df.dropna()
    output_df.to_csv('../DataSet/recommend_games.csv',
                     index=False,)
    
    
    
