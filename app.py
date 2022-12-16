from flask import Flask, render_template, url_for, session, redirect, request, flash, get_flashed_messages
from models import Pengguna, Transaksi
from datetime import datetime
import os

application = Flask(__name__)
application.config['SECRET_KEY'] = '1234567890!@#$%^&*()'
application.config['UPLOAD_FOLDER'] = os.path.realpath('.') + '/static/uploads'
application.config['MAX_CONTENT_PATH'] = 10000000

pengguna = Pengguna()
transaksi = Transaksi()

@application.route('/')
def index():
    if 'name' not in session:
        return redirect(url_for('login'))
    pemasukan = 50000
    pengeluaran = 10000
    persen = round((pengeluaran / pemasukan) * 100)
    data2 = (pemasukan, pengeluaran, persen)
    data = ()
    name = session.get('name')
    return render_template('dashboard.html', data=data, data2=data2, name=name)

@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username != '' and password != '':
            if len(username) > 3 and len(password) > 3:
                try:
                    data_user = pengguna.ambilDataUser(username, password)
                    session['pengguna_id'] = data_user[0]
                    session['name'] = data_user[1]
                    role = data_user[4]
                    if role == 'admin':
                        return redirect(url_for('dashboard_admin')) 

                    return redirect(url_for('index'))
                except:
                    return render_template('login.html', tidak_ada=True)
            else:
                return render_template('login.html', kurang=True)
        else:
            return render_template('login.html', kosong=True)

    if session.get('pesan') == 'registrasi_berhasil':
        session.pop('pesan','')
        return render_template('login.html', berhasil=True)
    return render_template('login.html')

@application.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        if username != '' and password != '':
            if len(username) > 3 and len(password) > 3:
                if pengguna.ambilDataUser(username, password) == None:
                    data = (name, username, password, 'user', '')
                    pengguna.insertDataUser(data)
                    session['pesan'] = 'registrasi_berhasil'
                    return redirect(url_for('login'))
                else:
                    return render_template('register.html', sudah_ada=True)
            else:
                return render_template('register.html', kurang=True)
        else:
            return render_template('register.html', kosong=True)
    return render_template('register.html')

@application.route('/show_note/<no>')
def show_note(no):
    return render_template('show_note.html', no=no)

@application.route('/dashboard_admin')
def dashboard_admin():
    name = session.get('name')
    total_user = pengguna.ambilTotalUser()
    data_user = pengguna.ambilSemuaDataUser()
    return render_template('dashboard_admin.html', name=name, total_user=total_user, data_user=data_user)

@application.route('/add_income', methods=['GET', 'POST'])
def add_income():
    if request.method == 'POST':
        pengguna_id = session.get('penguna_id')
        description = request.form['description']
        nominal = request.form['nominal']
        today = datetime.now().strftime('%Y-%m-%d')
        nota = request.files['nota']
        jumlah = str(transaksi.getCountTransaksiIdinDatabase())
        filename = application.config['UPLOAD_FOLDER'] + '/' + 'nota_' + jumlah
        if description != '' and nominal != '':
            if type(nominal) is int:
                print('sampai sini')
                try:
                    nota.save(filename)
                    filename = 'nota_' + jumlah
                    data = (pengguna_id, today, description, nominal, 0, filename)
                    transaksi.insertDataTransaksi(data)
                    return redirect(url_for('index'))
                except:
                    return render_template('add_income.html', gagal=True)
            else:
                return render_template('add_income.html', bukan_angka=True)
        else:
            return render_template('add_income.html', kosong=True)
    return render_template('add_income.html')

@application.route('/add_spending')
def add_spending():
    return render_template('add_spending.html', kosong=True)

@application.route('/edit_transaction')
def edit_transaction():
    return render_template('edit_transaction.html')

@application.route('/profile')
def profile():
    return render_template('profile.html', sukses=True)

@application.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html', kosong=True)

@application.route('/update/<no>')
def update(no):
    return render_template('login.html', no=no)

@application.route('/delete/<no>')
def delete(no):
    return render_template('login.html', no=no)

@application.route('/delete_user/<no>')
def delete_user(no):
    return render_template('dashboard_admin.html', no=no)

@application.route('/logout')
def logout():
    session.pop('name', '')
    session.pop('pengguna_id', '')
    return redirect(url_for('login'))

if __name__ == '__main__':
    application.run(debug=True)