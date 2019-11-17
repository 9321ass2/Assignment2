
from restapi import app




if __name__ == '__main__':
    import namespaces.authentication
    import namespaces.user

    app.run(debug=True)

