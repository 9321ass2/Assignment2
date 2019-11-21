import pandas as pd
from sklearn.utils import shuffle
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score


def train_rating_model():
    df = pd.read_csv("df_NOT_NULL.csv")
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
    return words ,ESRB_model,accuracy

def get_the_rating(pridict_array):
    dict = {1:'E',2:'E10',3:'M',4:'T',5:'EC',6:'KA',7:'AO',8:'RP'}
    words, ESRB_model , accuracy = train_rating_model()
    word_array = words.transform(pridict_array).toarray()
    key = ESRB_model.predict(word_array)
    key = key[0]
    rating = dict[key]
    print(rating)
    accuracy = f'{accuracy:.3}'
    print(accuracy)
    return rating ,accuracy

if __name__ == '__main__':
    #a example
    get_the_rating(['LEGO Indiana Jones: The Original Adventures Sports PS3  Zumba'])
