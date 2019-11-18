
from restapi import app




if __name__ == '__main__':
    import namespaces.authentication
    import namespaces.user
    import namespaces.predict
    app.run(debug=True)

