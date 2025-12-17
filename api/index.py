import sys
import os

# Fix path untuk Vercel serverless
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
backend_dir = os.path.join(parent_dir, 'Backend')

# Add to path
sys.path.insert(0, backend_dir)
sys.path.insert(0, parent_dir)

# Import Flask app - dengan lazy loading untuk serverless
try:
    # Change working directory to Backend
    os.chdir(backend_dir)
    
    # Import the Flask app
    from app import app
    
    # Disable init_db on import untuk serverless
    # Database akan di-init on demand
    
except Exception as e:
    # Fallback jika import gagal
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/api/<path:path>')
    def error(path):
        return jsonify({
            "error": "Backend import failed",
            "message": str(e),
            "path": sys.path[:3]
        }), 500

# Export for Vercel
app = app
