import sys
import os

# Fix path untuk import dari Backend
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(os.path.dirname(current_dir), 'Backend')
sys.path.insert(0, backend_dir)

# Set working directory
os.chdir(backend_dir)

# Import app
from app import app

# Vercel handler
app = app
