# develop: vmgabriel

import functools, jwt, datetime
from flask import jsonify

from config.server import configuration as conf

def compose(*functions):
     return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


def get_jwt(cookie):
    """Decode a Flask cookie."""
    def delete_first_four_in_token(content):
        return content.split(".")[0][4:]
    def delete_fisrt_and_last(content):
        return '.'.join(content.split(".")[1:-1])
    return delete_first_four_in_token(cookie) + '.' + delete_fisrt_and_last(cookie)


def verify_expiration(data):
     def seconds_counts_to_date(date):
          return datetime.datetime.fromtimestamp(date)
     return seconds_counts_to_date(data['exp']) > datetime.datetime.now()


def verify_ip(data, ip):
    return data == ip


def verify_permisssion(data, module, permission):
     def separe(separation):
          return lambda word: word.split(separation)

     def get_first(data):
          return data[0]

     def change_word(word_pre, word_pro):
          return lambda word: word_pro.join(word.split(word_pre))

     def do_all_in_array(fn):
          return lambda arr: [fn(arr[0])] if (len(arr) == 1) \
               else [fn(arr[0])] + do_all_in_array(fn)(arr[1:])

     def get_two_firsts_letters(word):
          return compose(
               ''.join,
               do_all_in_array(get_first),
               separe(' ')
          )(word)

     def filter_mod(mod):
          return lambda arr: [] if (len(arr) == 0) \
               else arr[0] if (arr[0][1] == mod) \
               else filter_mod(mod)(arr[1:])

     def is_in_array(perm):
          return lambda arr: False if (len(arr) == 0) \
               else True if (arr[0] == perm) \
               else is_in_array(perm)(arr[1:])

     get_module_valid = compose(
          filter_mod(module),
          do_all_in_array(separe('-')),
          separe('|'),
          change_word('.', ',')
     )
     get_perm_valid = compose(
          is_in_array(get_two_firsts_letters(permission)),
          separe(',')
     )

     module_data = get_module_valid(data['permission'])

     if (len(module_data) == 0):
          return False

     print(get_perm_valid(module_data[0]))
     if not get_perm_valid(module_data[0]):
          return False

     return True


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: json|string
    """
    try:
        payload = jwt.decode(auth_token, conf['jwt_secret'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def verify_cookie(cookies, ip, module, permission):
     cookie_auth = cookies.get('auth')

     if not cookie_auth:
          return jsonify({ 'code': 401, 'message': 'Token no Valid' }), 401

     data = compose(decode_auth_token, get_jwt)(cookie_auth)
     print('data - ', data)

     if type(data) == 'str':
          return jsonify({ 'code': 400, 'message': 'Token no Valid' }), 400

     # Verify Permissions
     if not verify_expiration(data):
          return jsonify({ 'code': 401, 'message': 'Token no Valid' }), 401

     # verify Permssion
     if not verify_permisssion(data, module, permission):
          return jsonify({ 'code': 403, 'message': 'Not Authorized' }), 403

     # Verify Ip
     if (conf['verify_ip']):
          if not verify_ip(data):
               return jsonify({ 'code': 401, 'message': 'Ip Not is Equal' }), 401

     # Hello  World
     if 'userId' in data and len(module.split(' ')) > 1:
          return data['userId']
