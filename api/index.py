import sys
import os

# Add Backend directory to path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Backend')
sys.path.insert(0, backend_path)
sys.path.insert(0, os.path.dirname(backend_path))

# Import Flask app
from app import app

# Export for Vercel
application = app
