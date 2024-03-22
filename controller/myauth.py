from flask_httpauth import HTTPBasicAuth
from model.mymodel import session, Users

auth = HTTPBasicAuth()

@auth.verify_password
def verify_credentials(username, password):
    # Query the database based on nama_user
    user = session.query(Users).filter_by(nama_users=username).first()
    
    # Return False if user not found
    if not user:
        return False

    # Compare NIK as password with stored NIK
    if password == user.NIK:
        return True
    return False
