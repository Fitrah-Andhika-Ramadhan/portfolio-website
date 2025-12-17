# 🔐 Login Tanpa Password - Panduan Setup

## ✅ Status Saat Ini

Admin user sudah berhasil dikonfigurasi di database dengan login **tanpa password**.

## 📝 Informasi Login

- **Username:** `admin`
- **Password:** (tidak diperlukan/kosong)

## 🚀 Cara Login

### Di Lokal
1. Pastikan server Flask running di `http://localhost:5000`
2. Buka `http://localhost:5000/admin.html`
3. Masukkan username: `admin`
4. Klik **Login** (jangan isi password)

### Di Production (Vercel)
1. Buka URL production Anda di `/admin.html`
2. Masukkan username: `admin`
3. Klik **Login** (jangan isi password)

## 🔧 Implementasi Teknis

### Backend (app.py)
```python
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    
    # Bypass password - hanya cek username
    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "access_token": access_token,
            "user": user.to_json()
        }), 200
    
    return jsonify({"error": "User not found"}), 401
```

### Frontend (admin.html)
- Form login hanya meminta **username**
- Tidak ada field password
- Pesan informatif: "Password login is disabled. Enter your username to continue."

## ✨ Fitur

- ✅ Login tanpa password
- ✅ Username sudah di-set ke "admin" sebagai default
- ✅ Token JWT otomatis di-generate
- ✅ Admin dashboard penuh fungsionalitas

## 🐛 Troubleshooting

### "User not found"
- Pastikan username benar: `admin`
- Cek database sudah terkoneksi dengan benar

### Server tidak respond
- Pastikan backend running
- Cek DATABASE_URL environment variable

### CORS Error
- Pastikan ALLOWED_ORIGINS include domain Anda
- Setting di backend/app.py sudah include '*' untuk development

## 📊 Manage Admin User

Jika perlu reset atau buat admin baru, jalankan:

```bash
cd Backend
python ensure_admin.py
```

Script ini akan:
1. Cek apakah admin user ada
2. Jika tidak ada, buat admin user baru
3. Tampilkan informasi login

---

**Last Updated:** 2025-12-17
**Status:** ✅ Fully Functional
