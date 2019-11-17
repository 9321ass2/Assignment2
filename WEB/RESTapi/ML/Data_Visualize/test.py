import pandas as pd 

# Test accuracy by checking difference between given & recommend 'Genre'.
knn = pd.read_csv('KNN.csv')
uf = pd.read_csv('user_favorite.csv')
rr = pd.read_csv('recommend_rank.csv')
genre_given = []
genre_recommend = []
for i in uf.itertuples():
    genre_given.append(knn[knn['Rank'] == i[1]]['Genre'].values[0])
for i in rr.itertuples():
    temp = knn[knn['Rank'] == i[2]]
    temp = temp.iloc[0]['Genre']
    genre_recommend.append(temp)
genre_given = list(set(genre_given))
print(genre_recommend)
genre_recommend = list(set(genre_recommend))
print(genre_given)
print('--------------------------------------')
print(genre_recommend)
