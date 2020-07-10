# Develop vmgabriel

# Interfaces
from domain.protocols.http import HttpProtocol
from domain.models.database_interface import Database_Interface
from user.applications.validate import User_Validate

from user.domain.user import User

# Libraries
from flask import Blueprint, jsonify, request
import datetime

class UserV0Http(HttpProtocol):
    def __init__(self, database_user: Database_Interface):
        self.name_table = 'users'
        self.database_user = database_user
        self.validate = User_Validate()

    def get_blueprint(self) ->  Blueprint:
        mod = Blueprint(self.name_table, __name__)

        @mod.route('/{}'.format(self.name_table), methods=['GET'])
        def getAll():
            order = request.args.get('order').split(',') if (request.args.get('order') != None) else []
            limit = 10 if (request.args.get('limit') == None) else request.args.get('limit')
            offset = 10 if (request.args.get('offset') == None) else request.args.get('offset')

            if (len(order) > 0):
                if not (self.validate.data_order_content(order)):
                    return jsonify({
                        'code': 400,
                        'error': 'order not valid'
                    }), 400

            (data, count) = self.database_user.get_all(limit, offset)

            return jsonify({
                'message': 'All Data',
                'count': count,
                'rows': data
            }), 200

        @mod.route('/{}/<int:id>'.format(self.name_table), methods=['GET'])
        def getOne(id):
            print('exec getOne - {}'.format(id))
            user_solicited = self.database_user.get_one(id)

            print('user_solicited - {}'.format(user_solicited))

            if not (user_solicited):
                return jsonify({ 'message': 'User not Found', 'data': {}  }), 200

            return jsonify({ 'message': 'User Found', 'data': user_solicited  }), 200

        @mod.route('/{}'.format(self.name_table), methods=['POST'])
        def create():
            if not request.is_json:
                return jsonify({ 'code': 400,'error': 'Data no Valid' }), 400

            data = request.get_json(force=True)

            data['id'] = 0
            data['isValid'] = True
            data['photoUrl'] = ''
            data['createdAt'] = data['updatedAt'] = data['deletedAt'] = datetime.datetime.now()

            (errors, new_user) = self.validate.validate_object(data)

            if not (errors == 'done correctly'):
                return jsonify({ 'error': errors, 'code': 400 }), 400

            saved_user = self.database_user.create(new_user)

            return jsonify({ 'message': 'created Correcly', 'data': saved_user  }), 201

        @mod.route('/{}/filter'.format(self.name_table), methods=['POST'])
        def filter():
            if not request.is_json:
                return jsonify({ 'code': 400,'error': 'Data no Valid' }), 400

            data = request.get_json(force=True)
            limit = 10 if (request.args.get('limit') == None) else request.args.get('limit')
            offset = 0 if (request.args.get('offset') == None) else request.args.get('offset')

            (data, count) = self.database_user.filter(
                data['filters'],
                data['attributes'],
                data['joins'],
                limit,
                offset
            )

            return jsonify({
                'message': 'Data Filtered',
                'count': count,
                'rows': data
            }), 200

        @mod.route('/{}/<int:id>'.format(self.name_table), methods=['PATCH'])
        def update(id):
            if not request.is_json:
                return jsonify({ 'code': 400,'error': 'Data no Valid' }), 400

            data = request.get_json(force=True)

            data['updatedAt'] = datetime.datetime.now()

            (errors, update_user) = self.validate.validate_object_update(data)

            if not (errors == 'done correctly'):
                return jsonify({ 'error': errors, 'code': 400 }), 400

            updated_user = self.database_user.update(update_user, id)

            return jsonify({ 'message': 'udpated correctly', 'data': updated_user }), 200

        @mod.route('/{}/<int:id>'.format(self.name_table), methods=['DELETE'])
        def delete(id):
            deleted_user = self.database_user.delete(id)

            return jsonify({ 'message': 'deleted correctly', 'data': deleted_user }), 200

        return mod
