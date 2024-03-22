from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()

# Mendefinisikan databse
class Users(db.Model):
    __tablename__ = 'users'

    id_users = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_users = db.Column(db.String(155), nullable=False)
    NIK = db.Column(db.String(16), nullable=False)
    alamat = db.Column(db.String(355), nullable=False)
    jenis_pajak = db.Column(db.Integer, nullable=False)
    nama_obyek_pajak = db.Column(db.String(155), nullable=False)
    NPWP = db.Column(db.String(10), nullable=False)
    pelaporan = db.relationship('Pelaporan', backref='users',cascade='all, delete-orphan', lazy=True)

    def __init__(self, nama_users, NIK, alamat, jenis_pajak, nama_obyek_pajak):
        self.nama_users = nama_users
        self.NIK = NIK
        self.alamat = alamat
        self.jenis_pajak = jenis_pajak
        self.nama_obyek_pajak = nama_obyek_pajak

        # Menghasilkan NPWP dari 6 digit pertama NIK dan jenis_pajak
        self.NPWP = (NIK)[:6] + str(jenis_pajak)

class Pelaporan(db.Model):
    __tablename__ = 'pelaporan'

    id_pelaporan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bulan_pelaporan = db.Column(db.Integer, nullable=False)
    bulan_pembayaran = db.Column(db.Integer, nullable=False)
    tahun_pelaporan = db.Column(db.Integer, nullable=False)
    tahun_pembayaran = db.Column(db.Integer)
    omst_jual = db.Column(db.Integer, nullable=False)
    id_users = db.Column(db.Integer, db.ForeignKey('users.id_users'))
    pajak_omst_jual = db.Column(db.Integer)
    keterlambatan = db.Column(db.Integer)
    total_pajak = db.Column(db.Integer)
    status_pembayaran = db.Column(db.Integer)

# Membuat engine
engine = create_engine('mysql://root@localhost/npwp')

# Membuat session SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()