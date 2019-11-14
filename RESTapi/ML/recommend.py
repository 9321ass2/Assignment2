import numpy as np
import pandas as pd


# Input is a simple array with virable length.
# Array contains serval numbers refer to rank of games.
def get_user_favorite():
    uf = pd.read_csv('./ML/Data_Visualize/user_favorite.csv')
    return uf


def get_all_games():
    ag = pd.read_csv('./ML/Data_Visualize/KNN.csv')
    return ag


def get_pop_games():
    pg = pd.read_csv('./ML/Data_Visualize/game_30.csv')
    return pg


def get_user_game_details(user_df, all_data):
    ESRB_list = []
    platform_list = []
    for i in user_df.itertuples():
        game_info = all_data[all_data['Rank'] == i[1]]
        ESRB_list.append(game_info['ESRB_Rating'].iloc[0])
        platform_list.append(game_info['Platform'].iloc[0])
        # print(game_info['Name'].iloc[0])
    ESRB_list = list(set(ESRB_list))
    platform_list = list(set(platform_list))
    return ESRB_list, platform_list


def get_gram_matrix():
    df = pd.read_csv('./ML/Data_Visualize/gram_matrix.csv')
    return df


def Recommand_Game():
    usr_game = get_user_favorite()
    all_game = get_all_games()
    pop_game = get_pop_games()
    ESRB_list, platform_list = get_user_game_details(usr_game, all_game)
    gram_matrix = get_gram_matrix()
    recommend_list = []
    target_list = list(np.array(usr_game)[:, 0])
    tar_num = len(target_list)
    for row in usr_game.itertuples():
        rank = row[1]
        matrix_column = rank - 1
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
                final_list.append((int(j[0]) + 1, j[1]))
                step += 1
                if step > 5:
                    break
    final_list = pd.DataFrame(final_list)
    final_list = final_list.sort_values(by=[1], ascending=False)
    # print(final_list)
    output = []
    for row in final_list.itertuples():
        if (row[1] not in output) and (row[1] not in target_list):
            output.append(row[1])
    output_df = pd.DataFrame(output)
    output_df.to_csv('./ML/Data_Visualize/recommend_rank.csv')
    return output_df
