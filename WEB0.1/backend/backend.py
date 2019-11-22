
from restapi import app,api_info,DataToday,country_df
from flask_cors import CORS



# def run(host, port):
#     if port is not None:
#         run1(host, port)
#     else:
#         for port in range(5000, 5100):
#             try:
#                 DataToday()
#                 app.run(debug=True, host=host, port=port)
#                 CORS(app)
#                 break
#             except OSError as e:
#                 if 'Address in use' in str(e):
#                     continue

if __name__ == '__main__':
    import namespaces.authentication
    import namespaces.user
    import namespaces.predict
    import namespaces.games
    import namespaces.country
    import namespaces.recom
    import namespaces.usage
    # host='127.0.0.1'
    # port=None
    # run(host, port)
    DataToday()
    app.run(debug=True)
    CORS(app)

