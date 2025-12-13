import redis
import time
import os

redis_host = os.environ.get('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

print("Worker siap menerima tugas...")

while True:
    # 1. Ambil tugas dari antrian (Blpop = Blocking Pop, tunggu sampai ada data)
    # Ini akan diam di sini kalau antrian kosong
    task = r.blpop('task_queue', timeout=0) 
    
    if task:
        print("Sedang memproses tugas berat...")
        time.sleep(5) # Simulasi kerja berat 5 detik
        print("Tugas Selesai!")