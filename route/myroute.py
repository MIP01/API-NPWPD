# Anda bisa menambahkan rute-rute tambahan di sini
from flask import Blueprint
from PBE.controller.myuser import get_users,get_udata,insert_users,delete_users,update_users
from controller.mylapor import get_data, get_idata, insert_data

users = Blueprint('users', __name__)
lapor = Blueprint('lapor', __name__)

# Routes for users
users.route('/', methods=['GET'])(get_users)
users.route('/<int:users_id>', methods=['GET'])(get_udata)
users.route('/insert', methods=['POST'])(insert_users)
users.route('/<int:users_id>', methods=['PUT'])(update_users)
users.route('/<int:users_id>', methods=['DELETE'])(delete_users)

# Routes for lapor
lapor.route('/all', methods=['GET'])(get_data)
lapor.route('/', methods=['GET'])(get_idata)
lapor.route('/insert', methods=['POST'])(insert_data)
