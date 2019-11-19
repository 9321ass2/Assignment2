from sklearn import linear_model
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder
import pandas as pd

def deal_with_df(Genre = None,Platform = None,Publisher = None): # deal with the df,to get the new df suit the require
    df = pd.read_csv('df_other.csv')
    if Genre != None :
        if Platform != None :
            if Publisher != None :
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
        if Platform != None :
            if Publisher != None :
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
    df3 = df['Name'].groupby(df['Year']).count()  #get the number of games in each year
    df3 = df3.to_frame()           
    df3 = shuffle(df3)
    df3.reset_index(level=0, inplace=True)   

    df_x = df3.drop('Name', axis=1).values       #get the value of x
    df_y = df3.drop('Year', axis=1).values       #get the value of y

    split_point = int(len(df_x) * 0.85)          #split x and y into train and test part
    X_train = df_x[:split_point]
    Y_train = df_y[:split_point]
    X_test = df_x[split_point:]
    Y_test = df_y[split_point:]

    model_linear = linear_model.LinearRegression() 
    model_linear.fit(X_train, Y_train)           #train the model
    pred_set = model_linear.predict(X_test)      
    score = r2_score(Y_test, pred_set)
    print(score)                                 #value the model
    return model_linear



if __name__ == '__main__':
    pd = deal_with_df(None , None , None)
    model = linear_machine_learning(pd)
    print(model.predict([[2020]]))
