from flask_restful import Resource
from listener.setup_handler import SetupHandler


class SetupResource(Resource):
    def __init__(self):
        self.handler: SetupHandler = SetupHandler()

    def head(self):
        self.handler.initialise_database()
        return {'message': 'Database initialised'}, 200
