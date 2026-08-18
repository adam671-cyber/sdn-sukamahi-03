from flask import Flask, render_template, request, redirect, url_for, session, flash
import functools
import google.generativeai as genai
import webbrowser
from threading import Timer

app = Flask(__name__)
app.secret_key = 'sk_sukamahi03_rahasia_super_aman'

# Konfigurasi API Key Gemini
import os
import sys
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Tentukan direktori dasar (Mendukung PyInstaller internal & Python normal)
if getattr(sys, 'frozen', False):
    # Jika dijalankan sebagai .exe (PyInstaller)
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    env_dir = os.path.dirname(sys.executable)
else:
    # Jika dijalankan biasa lewat python app.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    env_dir = base_dir

template_dir = os.path.join(base_dir, 'templates')
app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'rahasia_sekolah_sdn03'

# 2. Muat file .env dari folder tempat aplikasi berjalan
load_dotenv(os.path.join(env_dir, ".env"))

# 3. Ambil API Key & Konfigurasi
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    print("WARNING: API Key tidak ditemukan!")

# 4. Inisialisasi model Gemini
model = genai.GenerativeModel('gemini-3.6-flash')

USER_CREDENTIALS = {
    "admin": "sdn03sukamahi",
    "guru": "guru123"
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Silakan login terlebih dahulu untuk mengakses portal.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau password salah!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah keluar dari aplikasi.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    hasil = None
    form_data = {}

    if request.method == 'POST':
        mapel = request.form.get('mapel')
        jenjang = request.form.get('jenjang')
        topik = request.form.get('topik')
        jenis_output = request.form.get('jenis_output')
        jumlah = request.form.get('jumlah')

        form_data = {
            'mapel': mapel,
            'jenjang': jenjang,
            'topik': topik,
            'jenis_output': jenis_output,
            'jumlah': jumlah
        }

        prompt = (
            f"Anda adalah seorang guru dan penyusun RPP/Modul Ajar profesional.\n"
            f"Buatkan {jenis_output} untuk mata pelajaran {mapel} tingkat {jenjang} dengan topik {topik} sebanyak {jumlah}.\n\n"
            f"KETENTUAN KHUSUS APABILA MEMBUAT RPP/MODUL AJAR:\n"
            f"1. RPP harus dirancang khusus untuk **1 (satu) kali pertemuan** saja.\n"
            f"2. Gunakan istilah '8 Dimensi Profil Lulusan' (Keimanan dan Ketakwaan, Kewargaan, Penalaran Kritis, Kreativitas, Kolaborasi, Kemandirian, Kesehatan, Komunikasi).\n"
            f"3. Di bagian paling bawah dokumen RPP/Modul Ajar, WAJIB menyertakan lembar pengesahan/tanda tangan dengan format Markdown rapi persis seperti berikut:\n\n"
            f"```\n"
            f"                                                Cikarang Pusat, ......................\n"
            f"Mengetahui,\n"
            f"Kepala SDN Sukamahi 03                          Wali Kelas,\n\n\n\n"
            f"(__________________________)                    (__________________________)\n"
            f"NIP.                                            NIP.\n"
            f"```\n"
        )

        try:
            response = model.generate_content(prompt)
            hasil = response.text
        except Exception as e:
            hasil = f"Gagal menghasilkan dokumen. Error: {e}"

    return render_template('dashboard.html', hasil=hasil, form_data=form_data)

@app.route('/kurikulum', methods=['GET', 'POST'])
@login_required
def kurikulum():
    hasil = None
    form_data = {}

    if request.method == 'POST':
        mapel = request.form.get('mapel')
        jenjang = request.form.get('jenjang')
        topik = request.form.get('topik')
        jenis_output_kurikulum = request.form.get('jenis_output_kurikulum')
        jumlah = request.form.get('jumlah')

        form_data = {
            'mapel': mapel,
            'jenjang': jenjang,
            'topik': topik,
            'jenis_output_kurikulum': jenis_output_kurikulum,
            'jumlah': jumlah
        }

        prompt = (
            f"Anda adalah ahli penyusun kurikulum sekolah dasar. "
            f"Buatkan dokumen {jenis_output_kurikulum} untuk mata pelajaran {mapel} tingkat {jenjang}. "
            f"Cakupan Materi/Topik: {topik}. Target jumlah alokasi/poin: {jumlah}.\n\n"
            f"ATURAN PENTING KARAKTER LULUSAN:\n"
            f"JANGAN gunakan istilah 'Profil Pelajar Pancasila'. Gantikan dengan '8 Dimensi Profil Lulusan' (Deep Learning) yaitu: "
            f"Keimanan dan Ketakwaan, Kewargaan, Penalaran Kritis, Kreativitas, Kolaborasi, Kemandirian, Kesehatan, dan Komunikasi.\n"
            f"Jika dokumen berupa RPP, wajib diset untuk 1 kali pertemuan dan sertakan format tanda tangan Kepala Sekolah & Wali Kelas SDN Sukamahi 03 di bagian bawah.\n"
            f"Sajikan dalam bentuk tabel atau poin Markdown yang rapi dan komprehensif."
        )

        try:
            response = model.generate_content(prompt)
            hasil = response.text
        except Exception as e:
            hasil = f"Gagal menghasilkan dokumen kurikulum. Error: {e}"

    return render_template('kurikulum.html', hasil=hasil, form_data=form_data)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/dashboard")

@app.route('/shutdown', methods=['POST'])
def shutdown():
    # Fungsi untuk menghentikan aplikasi secara total di latar belakang
    def kill_server():
        os._exit(0)
    
    Timer(0.5, kill_server).start()
    return 'Aplikasi berhasil ditutup. Anda dapat menutup tab browser ini.'

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        Timer(1.5, open_browser).start()

    app.run(debug=True)