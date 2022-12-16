import pymysql
import config

database = cursor = None

class Pengguna():
    def __init__(self, pengguna_id=None, nama=None, username=None, password=None, role=None, bio=None,):
        self.pengguna_id = pengguna_id
        self.nama = nama
        self.username = username
        self.password = password
        self.role = role
        self.bio = bio

    def openDatabase(self):
        global database, cursor
        database = pymysql.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        cursor = database.cursor()

    def closeDatabase(self):
        global database, cursor
        database.close()

    def ambilDataUser(self, username, password):
        self.openDatabase()
        cursor.execute("SELECT * FROM pengguna WHERE username = '%s' AND password = '%s' " %
                       (username, password))
        data_user = cursor.fetchone()
        self.closeDatabase()
        return data_user

    def insertDataUser(self, data):
        self.openDatabase()
        cursor.execute(
            "INSERT INTO pengguna (nama, username, password) VALUES('%s', '%s', MD5('%s'))" % data)
        database.comit()
        self.closeDatabase

    def updateProfil(self, pengguna_id):
        self.openDatabase()
        cursor.execute(
            "UPDATE pengguna SET nama='%s', username='%s' , password=MD5('%s') , bio='%s' WHERE pengguna_id='%s' " % pengguna_id)
        database.commit()
        self.closeDatabase()

class Transaksi():
    def __init__(self, transaksi_id=None, pemasukan=None, pengeluaran=None, date=None, deskripsi=None, pengguna_id=None, upload_file=None):
        self.transaksi_id = transaksi_id
        self.pemasukan = pemasukan
        self.pengeluaran = pengeluaran
        self.date = date
        self.deskripsi = deskripsi
        self.pengguna_id = pengguna_id
        self.upload_file = upload_file
        
    def openDatabase(self):
        global database, cursor
        database = pymysql.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        cursor = database.cursor()

    def closeDatabase(self):
        global database, cursor
        database.close()

    def insertDataTransaksi(self, data):
        self.openDatabase()
        cursor.execute(
            "INSERT INTO transaksi (pengguna_id, date, deskripsi, pemasukan, pengeluaran, upload_file ) VALUES('%s', '%s', '%s','%s', '%s)" % data)
        database.comit()
        self.closeDatabase

    def ambilDataTransaksi(self, pengguna_id):
        self.openDatabase()
        cursor.execute(
            "SELECT * FROM transaksi WHERE pengguna_id = '%s'" % pengguna_id)
        data_user = cursor.fetchall()
        self.closeDatabase()
        return data_user

    def updateTransaksi(self, data):
        self.openDatabase()
        cursor.execute(
            "UPDATE transaksi SET deskripsi='%s', nominal='%s' , nota='%s' WHERE pengguna_id='%s' " % data)
        database.commit()
        self.closeDatabase()


    def deleteTransaksi(self, pengguna_id):
        self.openDatabase()
        cursor.execute(
            "DELETE FROM transaksi WHERE pengguna_id =%s" % pengguna_id)
        database.commit()
        self.closeDatabase()

    def getCountTransaksiIdinDatabase(self):
        self.openDatabase()
        cursor.execute(
            "SELECT COUNT(transaksi_id) FROM transaksi"
        )
        jumlah = cursor.fetchone()
        self.closeDatabase()
        return jumlah[0] + 1
