from flask_restplus import reqparse

access_token_parser = reqparse.RequestParser()
access_token_parser.add_argument('Authorization', help='Bearer <access_token>', location='headers')

refresh_parser = reqparse.RequestParser()
refresh_parser.add_argument('Authorization', help='Bearer <refresh_token>', location='headers')
