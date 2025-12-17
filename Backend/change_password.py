import os
from dotenv import load_dotenv
import psycopg2
from werkzeug.security import generate_password_hash

# Load environment
load_dotenv(os.path.join('..', '.env.local'))

# Database connection
db_url = os.getenv('DATABASE_URL') or 'postgresql://neondb_owner:npg_EnVuj8G4bmek@ep-hidden-thunder-adyxhuf2-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require'

print("🔐 Change Admin Password")
print("=" * 50)

# Get new password
new_password = input("\nMasukkan password baru untuk admin: ")
confirm_password = input("Konfirmasi password baru: ")

if new_password != confirm_password:
    print("❌ Password tidak cocok!")
    exit(1)

if len(new_password) < 6:
    print("❌ Password minimal 6 karakter!")
    exit(1)

try:
    # Connect to database
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    
    # Check if admin exists
    cursor.execute("""
        SELECT id FROM users 
        WHERE username = 'admin'
    """)
    
    admin = cursor.fetchone()
    
    if not admin:
        print("\n⚠️  User admin belum ada di database!")
        print("💡 Jalankan app.py terlebih dahulu untuk inisialisasi database")
        exit(1)
    
    # Hash password
    password_hash = generate_password_hash(new_password, method='pbkdf2:sha256')
    
    # Update password
    cursor.execute("""
        UPDATE users 
        SET password_hash = %s 
        WHERE username = 'admin'
    """, (password_hash,))
    
    conn.commit()
    print(f"\n✅ Password admin berhasil diubah!")
    print(f"   Username: admin")
    print(f"   Password: {new_password}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
