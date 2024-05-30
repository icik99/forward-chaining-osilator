# Flask CRUD Patient Project

This is a Flask-based web application for managing patient data. The application allows you to create, read, update, and delete patient records.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed [Python 3.x](https://www.python.org/downloads/).
- You have installed [Git](https://git-scm.com/).

## Getting Started

Follow these steps to get a copy of the project up and running on your local machine for development and testing purposes.

### 1. Clone Repository

```bash
git clone https://github.com/icik99/forward-chaining-osilator
```

### 2. Membuka GitBash

Ketika projek selesai di clone, klik kanan projek itu lalu klik **open git-bash here**


### 3. Setup Virtual Environtment

pertama inisiasi virtual environtment:
```bash
python -m venv venv
```

kedua aktifkan virtual environtment:
```bash
source venv/Scripts/activate
```

### 4. Install Dependensi

Install dependency dengan command:
```bash
pip install -r requirements.txt
```

### 5. Setup Database

1. Untuk setup database, perlu menginstall xampp terlebih dahulu, lalu pada bagian module **Apache** dan **MySQL** di klik **Start**
2. Jika apache dan mysql telah berjalan, buka link http://localhost/phpmyadmin/
3. Buat database baru dengan nama _osilator_db_
4. Lalu pada gitbash yang telah dibuka sebelumnya, copy command ini:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

### 6. Jalankan Projek

Pada gitbash, ketikkan command ini:
```bash
Python run.py
```

Ketika berhasil di run, nanti pada command gitbash akan ada url localhostxxx, copy URL itu untuk melihat web yang sudah di clone.

