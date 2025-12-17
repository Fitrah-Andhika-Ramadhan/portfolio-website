#!/usr/bin/env python3
"""
Script untuk memastikan admin user ada di database dan test login tanpa password
"""
import os
from dotenv import load_dotenv
from app import app, db
from models import User
import requests

# Load environment variables
load_dotenv()

def ensure_admin_user():
    """Memastikan admin user ada di database"""
    with app.app_context():
        # Cek apakah admin sudah ada
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            print("✅ Admin user sudah ada di database")
            print(f"   - Username: {admin.username}")
            print(f"   - Email: {admin.email}")
            print(f"   - Is Admin: {admin.is_admin}")
            return True
        else:
            # Buat admin user baru
            print("⚙️  Membuat admin user baru...")
            admin = User(
                username='admin',
                email='admin@portfolio.com',
                is_admin=True
            )
            admin.set_password('admin123')  # Set password meski tidak dipakai
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user berhasil dibuat")
            print(f"   - Username: admin")
            print(f"   - Email: admin@portfolio.com")
            return True

def test_login():
    """Test login tanpa password"""
    print("\n🧪 Testing login tanpa password...")
    
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')
    
    try:
        # Test login dengan username saja (tanpa password)
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"username": "admin"},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login berhasil!")
            print(f"   - Token: {result['access_token'][:50]}...")
            print(f"   - User: {result['user']}")
        else:
            print(f"❌ Login gagal: {response.status_code}")
            print(f"   - Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("⚠️  Tidak bisa connect ke API server")
        print(f"   - Pastikan server running di {BASE_URL}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🔐 ADMIN USER SETUP & LOGIN TEST")
    print("=" * 60)
    
    ensure_admin_user()
    
    print("\n" + "=" * 60)
    print("📝 INFORMASI LOGIN")
    print("=" * 60)
    print("Username: admin")
    print("Password: (tidak diperlukan)")
    print("\n✨ Cukup masukkan username 'admin' untuk login!")
    print("=" * 60)
