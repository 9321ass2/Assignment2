import pandas as pd 

# Test accuracy by checking difference between given & recommend 'Genre'.
knn = pd.read_csv('./ML/Data_Visualize/KNN.csv')
uf = pd.read_csv('./ML/DataSet/user_favorite.csv')
rr = pd.read_csv('./ML/DataSet/recommend_games.csv')
genre_given = []
genre_recommend = []
for i in uf.itertuples():
    genre_given.append(knn[knn['Rank'] == i[1]]['Genre'].values[0])
for i in rr.itertuples():
    genre_recommend.append(knn[knn['Rank'] == i[1]]['Genre'].values[0])
genre_given = set(genre_given)
genre_recommend = set(genre_recommend)

accuracy = (len(genre_given) - len(genre_given -
                                   genre_recommend)) / len(genre_given)
print(f'Accuracy = {round(accuracy, 4)*100}%')
