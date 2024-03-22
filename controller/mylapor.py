from model.mymodel import session, Users, Pelaporan
from flask import jsonify, request
from controller.myauth import auth


def get_data():
    data = session.query(Pelaporan).all()
    data_list = []

    for pelaporan in data:
        users = session.query(Users).filter_by(id_users=pelaporan.id_users).first()
        if users:
            pelaporan_data = {
                'NPWP': users.NPWP,
                'nama_obyek_pajak': users.nama_obyek_pajak,
                'bulan_pelaporan': pelaporan.bulan_pelaporan,
                'bulan_pembayaran': pelaporan.bulan_pembayaran,
                'tahun_pelaporan': pelaporan.tahun_pelaporan,
                'tahun_pembayaran': pelaporan.tahun_pembayaran,
                'omst_jual': pelaporan.omst_jual,
                'pajak_omst_jual': pelaporan.pajak_omst_jual,
                'keterlambatan': pelaporan.keterlambatan,
                'total_pajak': pelaporan.total_pajak,
                'status_pembayaran': pelaporan.status_pembayaran
            }
            data_list.append(pelaporan_data)

    return jsonify(data_list)

@auth.login_required
def get_idata():
    current_user = auth.current_user()
    user = session.query(Users).filter_by(nama_users=current_user).first()
    if not user:
        return jsonify({'message': 'Pengguna tidak ditemukan'})

    data_list = []
    pelaporans = session.query(Pelaporan).filter_by(id_users=user.id_users).all()
    if not pelaporans:
        return jsonify({'message': 'Data tidak ditemukan'})

    for data in pelaporans:
        pelaporan_data = {
            'NPWP': user.NPWP,
            'nama_obyek_pajak': user.nama_obyek_pajak,
            'bulan_pelaporan': data.bulan_pelaporan,
            'bulan_pembayaran': data.bulan_pembayaran,
            'tahun_pelaporan': data.tahun_pelaporan,
            'tahun_pembayaran': data.tahun_pembayaran,
            'omst_jual': data.omst_jual,
            'pajak_omst_jual': data.pajak_omst_jual,
            'keterlambatan': data.keterlambatan,
            'total_pajak': data.total_pajak,
            'status_pembayaran': data.status_pembayaran
        }
        data_list.append(pelaporan_data)

    return jsonify(data_list)


@auth.login_required
def insert_data():
    # Dapatkan pengguna yang saat ini diautentikasi
    current_user = auth.current_user()
    # Dapatkan jenis pajak dari pengguna
    user = session.query(Users).filter_by(nama_users=current_user).first()
    jenis_pajak = user.jenis_pajak

    data = request.get_json()
    bulan_pelaporan = data.get('bulan_pelaporan')
    bulan_pembayaran = data.get('bulan_pembayaran')
    tahun_pelaporan = data.get('tahun_pelaporan')
    tahun_pembayaran = data.get('tahun_pembayaran')
    omst_jual = data.get('omst_jual')

    if bulan_pelaporan is not None and tahun_pelaporan is not None and omst_jual is not None:
        # Dapatkan id_penjual dari tabel Penjual berdasarkan username yang diautentikasi
        users = session.query(Users).filter_by(nama_users=current_user).first()
        id_users = users.id_users

        if omst_jual is not None:
            # Menghitung pajak omset (10% dari omset penjualan)
            omst_jual = float(omst_jual)
            pajak_omst_jual = 0.1 * omst_jual

            # Hitung total_pajak
            total_pajak = pajak_omst_jual

            # Hitung keterlambatan
            if bulan_pembayaran == 0:
                tahun_pembayaran = 0

            if tahun_pembayaran > tahun_pelaporan and bulan_pembayaran <= bulan_pelaporan:
                keterlambatan = (12 - bulan_pelaporan) + bulan_pembayaran
            elif tahun_pembayaran > tahun_pelaporan and bulan_pembayaran > bulan_pelaporan:
                keterlambatan = 12 + (bulan_pembayaran - bulan_pelaporan)
            else:
                keterlambatan = max(0, bulan_pembayaran - bulan_pelaporan)

            # Atur status pembayaran
            status_pembayaran = 0 if bulan_pembayaran == 0 else 1
            
            if bulan_pelaporan <= bulan_pembayaran:
                # Hitung denda berdasarkan jenis pajak
                if jenis_pajak == 1:
                    denda = 0.01  
                elif jenis_pajak == 2:
                    denda = 0.02  
                elif jenis_pajak == 3:
                    denda = 0.005  

                # Hitung jumlah denda berdasarkan omset penjualan
                total_denda = denda * omst_jual * keterlambatan
                total_pajak += total_denda  # Tambahkan total_denda ke total_pajak

            new_lapor = Pelaporan(bulan_pelaporan=bulan_pelaporan, tahun_pelaporan=tahun_pelaporan,tahun_pembayaran=tahun_pembayaran, omst_jual=omst_jual, bulan_pembayaran=bulan_pembayaran, pajak_omst_jual=pajak_omst_jual, total_pajak=total_pajak,keterlambatan=keterlambatan, status_pembayaran=status_pembayaran, id_users=id_users)
            session.add(new_lapor)
            session.commit()
            return jsonify({'message': 'Data berhasil dimasukkan ke database'})
    else:
        return jsonify({'message': 'Data tidak lengkap'})
