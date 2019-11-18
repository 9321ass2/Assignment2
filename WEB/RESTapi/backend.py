
from restapi import app,api_info,DataToday
from flask_cors import CORS



if __name__ == '__main__':
    import namespaces.authentication
    import namespaces.user
    import namespaces.predict
    import namespaces.data
    DataToday()
    app.run(debug=True)
    CORS(app)
