from model.mymodel import session, Users
from flask import jsonify, request
from controller.myauth import auth
from sqlalchemy.exc import IntegrityError


def get_users():
    data = session.query(Users).all()
    data_list = []

    for users in data:
        users_data = {
            'id_users': users.id_users,
            'nama_users': users.nama_users,
            'NIK' : users.NIK,
            'alamat' : users.alamat,
            'jenis_pajak' : users.jenis_pajak,
            'nama_obyek_pajak': users.nama_obyek_pajak,
            'NPWP' : users.NPWP
        }
        data_list.append(users_data)

    return jsonify(data_list)

@auth.login_required
def get_udata(users_id):
    current_user = auth.current_user()  # Mendapatkan nama pengguna yang diautentikasi
    data = session.query(Users).filter_by(id_users=users_id).first()
    
    if data:
        # Memeriksa apakah pengguna saat ini adalah pemilik data yang akan diakses
        if current_user == data.nama_users:
            users_data = {
                'id_users': data.id_users,
                'nama_users': data.nama_users,
                'NIK': data.NIK,
                'alamat': data.alamat,
                'jenis_pajak': data.jenis_pajak,
                'nama_obyek_pajak': data.nama_obyek_pajak,
                'NPWP': data.NPWP,
            }
            return jsonify([users_data])
        else:
            return jsonify({'message': 'Anda tidak diizinkan mengakses data ini'}), 403  # Forbidden
    else:
        return jsonify({'message': 'Pengguna tidak ditemukan'}), 404  # Not Found
    
def insert_users():
    try:
        data = request.get_json()
        nama_users = data.get('nama_users')
        NIK = data.get('NIK')
        alamat = data.get('alamat')
        jenis_pajak = data.get('jenis_pajak')
        nama_obyek_pajak = data.get('nama_obyek_pajak')
            
        if nama_users is not None and NIK is not None and alamat is not None and jenis_pajak is not None and nama_obyek_pajak is not None:
            new_users = Users(nama_users=nama_users,NIK=NIK,alamat=alamat, jenis_pajak=jenis_pajak, nama_obyek_pajak=nama_obyek_pajak)
            session.add(new_users)
            session.commit()
            return jsonify({'message': 'Data berhasil dimasukkan ke database'})
        else:
            return jsonify({'message': 'Data yang diberikan tidak lengkap'})
    except IntegrityError:
        session.rollback()
        return jsonify({'message': "Nama sudah ada"})
    
@auth.login_required
def update_users(users_id):
    current_user = auth.current_user()  # Mendapatkan nama pengguna yang diautentikasi
    data = session.query(Users).filter_by(id_users=users_id).first()

    if data:
        # Memeriksa apakah pengguna saat ini adalah pemilik data yang akan diperbarui
        if current_user == data.nama_users:
            update = request.get_json()
            nama_users = update.get('nama_users')
            NIK = update.get('NIK')
            alamat = update.get('alamat')
            jenis_pajak = update.get('jenis_pajak')
            nama_obyek_pajak = update.get('nama_obyek_pajak')
            
            if nama_users:
                data.nama_users = nama_users
            if NIK:
                data.NIK = NIK
            if alamat:
                data.alamat = alamat
            if jenis_pajak:
                data.jenis_pajak = jenis_pajak
            if nama_obyek_pajak:
                data.nama_obyek_pajak = nama_obyek_pajak

            session.commit()
            return jsonify({'message': 'Data berhasil diperbarui'})
        else:
            return jsonify({'message': 'Anda tidak diizinkan memperbarui data ini'}), 403  # Forbidden
    else:
        return jsonify({'message': 'Data tidak ditemukan'}), 404  # Not Found

@auth.login_required   
def delete_users(users_id):
    current_user = auth.current_user()  # Mendapatkan nama pengguna yang diautentikasi
    data = session.query(Users).filter_by(id_users=users_id).first()

    if data:
        users = session.query(Users).filter_by(nama_users=current_user).first()
        if data.id_users == users.id_users:
            # Hapus data jika ditemukan
            session.delete(data)
            session.commit()
            return jsonify({'message': 'Data berhasil dihapus'})
        else:
                return jsonify({'message': 'Anda tidak diizinkan menghapus data ini'})
    else:
        return jsonify({'message': 'Data tidak ditemukan'})