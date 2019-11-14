
from restapi import app
from ML.gram_matrix import Create_Final_Matrix



if __name__ == '__main__':
    import namespaces.authentication
    import namespaces.user

    app.run(debug=True)

