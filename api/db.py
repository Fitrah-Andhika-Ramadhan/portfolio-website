import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(
        os.environ.get('DATABASE_URL'),
        cursor_factory=RealDictCursor
    )

def query_one(sql, params=None):
    """Execute query and return one result"""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        result = cur.fetchone()
        cur.close()
        return dict(result) if result else None
    finally:
        conn.close()

def query_all(sql, params=None):
    """Execute query and return all results"""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        results = cur.fetchall()
        cur.close()
        return [dict(row) for row in results]
    finally:
        conn.close()

def execute(sql, params=None, fetch=False):
    """Execute query with commit"""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        
        if fetch:
            result = cur.fetchone()
            result = dict(result) if result else None
        else:
            result = cur.rowcount
            
        conn.commit()
        cur.close()
        return result
    finally:
        conn.close()
