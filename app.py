from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()


class Database(Resource):
    def updateDb(self, name, is_looking):

        my_string = ""
        f = open("database.txt", "r")
        temp = f.read().splitlines()
        for x in temp:
            user_info = x.split(",")
            if user_info[0] == name:
                user_info[1] = is_looking
            my_string += (user_info[0] + "," + user_info[1] + "\n")
        f.close()

        f = open("database.txt", "w")
        f.write(my_string)
        f.close()

    def get(self):
        f = open("database.txt", "r")
        users_looking = []
        temp = f.read().splitlines()
        for x in temp:
            userInfo = x.split(",")
            if userInfo[1] == "1":
                users_looking.append(userInfo[0])
        f.close()
        return users_looking, 200

    def post(self):
        parser.add_argument('name', type=str)
        parser.add_argument('seeking', type=str)
        args = parser.parse_args()
        name = args.get('name')
        seeking = args.get('seeking')
        if not name.isalpha():
            return {
                'status': "Error: Invalid name argument, must only contain alphabet characters'"
            }, 400
        if seeking != "true" and seeking != "false":
            return {
                'status': "Error: Invalid seeking argument, must be 'true' or 'false'"
            }, 400
        self.updateDb(name=name, is_looking=seeking)

        return {
            'status': seeking,
            'name': name
        }, 200

api.add_resource(Database, "/looking-for-chat")

if __name__ == '__main__':
    app.run(debug=True)
