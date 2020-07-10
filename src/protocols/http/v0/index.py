# Develop vmgabriel

# Libraries
from flask import Blueprint, jsonify

mod = Blueprint('api', __name__)

# Define Route Base
@mod.route('/')
def health_check():
    return jsonify({ 'code': 200, 'mesage': 'Daga User Service' })

# define About me
@mod.route('/aboutme')
def about_me():
    return jsonify({ 'code': 200, 'message': 'created for vmgabriel, dbgroldan' })
