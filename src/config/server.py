# Develop Vmgabriel

import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

configuration = {
    'host': '0.0.0.0',
    'port': 7202,

    'debug': True,

    'cookie_secret': os.getenv('COOKIE_SECRET'),
    'cookie_name': os.getenv('COOKIE_NAME'),

    'jwt_location': ['cookies'],
    'jwt_secret': os.getenv('JWT_SECRET'),

    'verify_ip': False, # True | False

    'limit_max': 200,
    'limit_min': 0,

    'db_name_database': 'db_daga_test',
    'db_name_schema': 'daga_test',
    'user_database': os.getenv('USER_DATABASE'),
    'password_database': os.getenv('PASSWORD_DATABASE'),
    'host_database': os.getenv('HOST_DATABASE'),
    'port_database': '5432',

    'persistency': 'postgres'
}
