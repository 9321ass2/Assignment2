from sklearn import linear_model
from sklearn.utils import shuffle
from sklearn.metrics import r2_score
import pandas as pd

import pandas as pd
from sklearn.utils import shuffle
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score


def train_rating_model():
    df = pd.read_csv("./ML/DataSet/df_NOT_NULL.csv")
    df = shuffle(df)
    ESRB_x = df.drop('ESRB_Rating', axis=1)
    ESRB_x = ESRB_x.drop('Rank', axis=1)
    ESRB_x = ESRB_x.drop('basename', axis=1).values
    ESRB_y = df['ESRB_Rating'].values
    ESRB_x = pd.DataFrame(ESRB_x)
    ESRB_y = pd.DataFrame(ESRB_y)
    for i in range(6):
        ESRB_x[i] = ESRB_x[i].map(str)

    for i in range(1, 6):
        ESRB_x[0] = ESRB_x[0].str.cat(ESRB_x[i], sep=' ')

    ESRB_x = ESRB_x[0]

    length = ESRB_x.shape[0]

    words = CountVectorizer(token_pattern=r'[A-Za-z0-9:]{1,}', lowercase=False)
    bag_of_words = words.fit_transform(ESRB_x)
    sentence_array = bag_of_words.toarray()

    ESRB_y[0] = ESRB_y[0].map(str)
    ESRB_y.replace('E', 1, inplace=True)
    ESRB_y.replace('E10', 2, inplace=True)
    ESRB_y.replace('M', 3, inplace=True)
    ESRB_y.replace('T', 4, inplace=True)
    ESRB_y.replace('EC', 5, inplace=True)
    ESRB_y.replace('KA', 6, inplace=True)
    ESRB_y.replace('AO', 7, inplace=True)
    ESRB_y.replace('RP', 8, inplace=True)

    ESRB_y = ESRB_y.astype('int')

    ESRB_X_train = sentence_array[:int(length * 0.8)]
    ESRB_X_test = sentence_array[int(length * 0.8):]
    ESRB_y_train = ESRB_y[:int(length * 0.8)]
    ESRB_y_test = ESRB_y[int(length * 0.8):]

    ESRB_model = MultinomialNB(alpha=1, class_prior=None, fit_prior=True)
    ESRB_model = ESRB_model.fit(ESRB_X_train, ESRB_y_train)
    pred_set = ESRB_model.predict(ESRB_X_test)
    accuracy = accuracy_score(ESRB_y_test, pred_set)
    return words, ESRB_model, accuracy


def get_the_rating(pridict_array):
    dict = {1: 'E', 2: 'E10', 3: 'M', 4: 'T', 5: 'EC', 6: 'KA', 7: 'AO', 8: 'RP'}
    words, ESRB_model, accuracy = train_rating_model()
    word_array = words.transform(pridict_array).toarray()
    key = ESRB_model.predict(word_array)
    key = key[0]
    rating = dict[key]
    accuracy = f'{accuracy:.3}'
    return rating, accuracy


def deal_with_df(Genre=None, Platform=None, Publisher=None):  # deal with the df,to get the new df suit the require
    df = pd.read_csv('./ML/DataSet/df_other.csv')
    if Genre != None:
        if Platform != None:
            if Publisher != None:
                df2 = df[df['Genre'] == Genre]
                df2 = df2[df2['Platform'] == Platform]
                df2 = df2[df2['Publisher'] == Publisher]
            else:
                df2 = df[df['Genre'] == Genre]
                df2 = df2[df2['Platform'] == Platform]
        else:
            if Publisher != None:
                df2 = df[df['Genre'] == Genre]
                df2 = df2[df2['Publisher'] == Publisher]
            else:
                df2 = df[df['Genre'] == Genre]
    else:
        if Platform != None:
            if Publisher != None:
                df2 = df[df['Platform'] == Platform]
                df2 = df2[df2['Publisher'] == Publisher]
            else:
                df2 = df[df['Platform'] == Platform]
        else:
            if Publisher != None:
                df2 = df[df['Publisher'] == Publisher]
            else:
                return df
    return df2


def linear_machine_learning(df):
    df3 = df['Name'].groupby(df['Year']).count()  # get the number of games in each year
    df3 = df3.to_frame()
    df3 = shuffle(df3)
    df3.reset_index(level=0, inplace=True)

    df_x = df3.drop('Name', axis=1).values  # get the value of x
    df_y = df3.drop('Year', axis=1).values  # get the value of y

    split_point = int(len(df_x) * 0.85)  # split x and y into train and test part
    X_train = df_x[:split_point]
    Y_train = df_y[:split_point]
    X_test = df_x[split_point:]
    Y_test = df_y[split_point:]

    model_linear = linear_model.LinearRegression()
    model_linear.fit(X_train, Y_train)  # train the model
    pred_set = model_linear.predict(X_test)
    score = r2_score(Y_test, pred_set)
    accuracy = f'{score:.3}'
    return model_linear, accuracy


def linear_predict(Genre=None, Platform=None, Publisher=None, year=2020):
    pd_out = deal_with_df(Genre, Platform, Publisher)
    model, accuracy = linear_machine_learning(pd_out)
    games = int(model.predict([[year]])[0][0])
    if float(accuracy) < 0.3:
        accuracy = 'LOW'
    elif float(accuracy) < 0.6:
        accuracy = 'MEDIUM'
    else:
        accuracy = 'HIGH'
    return {'prediction_amount_of_games': games, 'accuracy': accuracy}


def ESRB_predict(text):
    rating,accuracy = get_the_rating(text)
    if float(accuracy) < 0.3:
        accuracy = 'LOW'
    elif float(accuracy) < 0.6:
        accuracy = 'MEDIUM'
    else:
        accuracy = 'HIGH'
    return {'predict_ESRB':rating, 'accuracy': accuracy}