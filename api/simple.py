from flask import Flask, jsonify
import sys
import os

app = Flask(__name__)

@app.route('/')
@app.route('/api/test')
def test():
    return jsonify({
        "status": "ok",
        "message": "Simple Flask app running on Vercel!",
        "python_version": sys.version,
        "cwd": os.getcwd(),
        "files": os.listdir('.')[:10]
    })

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "service": "taskmaster-api"})

# For Vercel
app = app
