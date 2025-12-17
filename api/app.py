from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from functools import wraps
import jwt
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from .db import query_one, query_all, execute

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-key')

# CORS
allowed_origins = os.environ.get('ALLOWED_ORIGINS', '*').split(',')
CORS(app, origins=allowed_origins if allowed_origins != ['*'] else '*', supports_credentials=True)

# Auth decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token missing'}), 401
        
        try:
            token = token.replace('Bearer ', '')
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = query_one('SELECT * FROM users WHERE id = %s', (data['user_id'],))
            if not current_user:
                return jsonify({'message': 'Invalid token'}), 401
        except:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# ============= ROUTES =============

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get portfolio statistics"""
    try:
        stats = {
            'total_projects': query_one('SELECT COUNT(*) as count FROM projects')['count'],
            'total_skills': query_one('SELECT COUNT(*) as count FROM skills')['count'],
            'total_experiences': query_one('SELECT COUNT(*) as count FROM experiences')['count'],
            'total_articles': query_one('SELECT COUNT(*) as count FROM articles WHERE published = true')['count']
        }
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    try:
        categories = query_all('SELECT * FROM categories ORDER BY name')
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get projects with filters"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 9))
        category = request.args.get('category', 'all')
        search = request.args.get('search', '')
        sort = request.args.get('sort', 'created_at')
        
        offset = (page - 1) * per_page
        
        # Build query
        where = []
        params = []
        
        if category != 'all':
            where.append('category_id = %s')
            params.append(category)
        
        if search:
            where.append("(title ILIKE %s OR description ILIKE %s)")
            params.extend([f'%{search}%', f'%{search}%'])
        
        where_clause = 'WHERE ' + ' AND '.join(where) if where else ''
        
        # Sort
        order_map = {
            'created_at': 'created_at DESC',
            'title': 'title ASC',
            'likes': 'likes DESC'
        }
        order_by = order_map.get(sort, 'created_at DESC')
        
        # Count total
        count_sql = f'SELECT COUNT(*) as count FROM projects {where_clause}'
        total = query_one(count_sql, params)['count']
        
        # Get projects
        sql = f'''
            SELECT p.*, c.name as category_name 
            FROM projects p
            LEFT JOIN categories c ON p.category_id = c.id
            {where_clause}
            ORDER BY p.{order_by}
            LIMIT %s OFFSET %s
        '''
        params.extend([per_page, offset])
        projects = query_all(sql, params)
        
        return jsonify({
            'projects': projects,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get all skills"""
    try:
        skills = query_all('SELECT * FROM skills ORDER BY proficiency DESC, name')
        return jsonify(skills), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/experiences', methods=['GET'])
def get_experiences():
    """Get all experiences"""
    try:
        experiences = query_all('SELECT * FROM experiences ORDER BY start_date DESC')
        return jsonify(experiences), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """Get published articles"""
    try:
        per_page = int(request.args.get('per_page', 6))
        articles = query_all(
            'SELECT * FROM articles WHERE published = true ORDER BY published_at DESC LIMIT %s',
            (per_page,)
        )
        return jsonify(articles), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Admin login"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        user = query_one('SELECT * FROM users WHERE username = %s', (username,))
        
        if user and check_password_hash(user['password_hash'], password):
            token = jwt.encode({
                'user_id': user['id'],
                'exp': datetime.utcnow() + timedelta(days=7)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            return jsonify({
                'token': token,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'is_admin': user['is_admin']
                }
            }), 200
        
        return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard', methods=['GET'])
@token_required
def get_dashboard(current_user):
    """Get admin dashboard data"""
    try:
        data = {
            'stats': {
                'total_projects': query_one('SELECT COUNT(*) as count FROM projects')['count'],
                'total_skills': query_one('SELECT COUNT(*) as count FROM skills')['count'],
                'total_experiences': query_one('SELECT COUNT(*) as count FROM experiences')['count'],
                'total_contacts': query_one('SELECT COUNT(*) as count FROM contacts')['count']
            },
            'recent_contacts': query_all('SELECT * FROM contacts ORDER BY created_at DESC LIMIT 5')
        }
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200
