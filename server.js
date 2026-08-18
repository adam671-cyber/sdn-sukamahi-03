const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// 1. Set EJS sebagai Template Engine & Folder Views
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// 2. Folder Publik (CSS/Assets) & Uploads
app.use(express.static(path.join(__dirname, 'public')));
app.use('/uploads', express.static(path.join(__dirname, 'public/uploads')));
app.use(express.urlencoded({ extended: true }));

// 3. Membuat folder public/uploads otomatis jika belum ada
const uploadDir = path.join(__dirname, 'public/uploads');
if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir, { recursive: true });
}

// 4. Konfigurasi Multer untuk Unggah File (PDF, Docx, Excel, APK, Gambar)
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'public/uploads/');
    },
    filename: (req, file, cb) => {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, uniqueSuffix + path.extname(file.originalname));
    }
});

const fileFilter = (req, file, cb) => {
    const allowedExtensions = ['.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.apk', '.jpg', '.jpeg', '.png'];
    const ext = path.extname(file.originalname).toLowerCase();
    if (allowedExtensions.includes(ext)) {
        cb(null, true);
    } else {
        cb(new Error('Format file tidak didukung!'), false);
    }
};

const upload = multer({ storage: storage, fileFilter: fileFilter });

// 5. Data Sementara (In-Memory Data)
let dataMateri = [
    { title: 'Modul Matematika Kelas 4', category: 'Matematika', fileUrl: '/uploads/sample-math.pdf', filename: 'Modul_MTK_K4.pdf' }
];

let dataAplikasi = [
    { title: 'Aplikasi Pembelajaran Android', version: '1.0', fileUrl: '/uploads/app-learning.apk', filename: 'Edukasi_SDN03.apk' },
    
    // TAMBAHKAN APLIKASI PYTHON KAMU DI SINI:
    { title: 'Portal Pembelajaran Python (PC)', version: '1.0', fileUrl: '/uploads/Portal-Pembelajaran.zip', filename: 'Portal-Pembelajaran.zip' }
];

// 6. ROUTING (Jalur Halaman Web)

// Halaman Beranda Utama
app.get('/', (req, res) => {
    res.render('index', { title: 'Beranda - SDN Sukamahi 03' });
});

// Halaman E-Learning & Materi
app.get('/e-learning', (req, res) => {
    res.render('e-learning', { title: 'E-Learning - SDN Sukamahi 03', materis: dataMateri });
});

// Proses Upload Materi Baru
app.post('/upload-materi', upload.single('fileMateri'), (req, res) => {
    if (req.file) {
        dataMateri.push({
            title: req.body.judul,
            category: req.body.kategori,
            fileUrl: '/uploads/' + req.file.filename,
            filename: req.file.originalname
        });
    }
    res.redirect('/e-learning');
});

// Halaman Pusat Unduhan Aplikasi & Dokumen
app.get('/download-center', (req, res) => {
    res.render('download', { title: 'Pusat Unduhan - SDN Sukamahi 03', apps: dataAplikasi });
});

// 7. Menjalankan Server
app.listen(PORT, () => {
    console.log(`Server SDN Sukamahi 03 berjalan di http://localhost:${PORT}`);
});