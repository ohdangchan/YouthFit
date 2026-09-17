import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')

from scripts import db_connection

def setup_users_table():
    conn, db_type = db_connection.get_connection(allow_sqlite_fallback=True)
    cur = conn.cursor()

    print(f"Connected to {db_type.upper()} database.")

    # PostgreSQL / SQLite users table schema
    if db_type == "postgresql":
        create_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            password_hash VARCHAR(255),
            provider VARCHAR(50) DEFAULT 'local',
            profile_json JSONB DEFAULT '{}',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        """
    else:
        create_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT,
            provider TEXT DEFAULT 'local',
            profile_json TEXT DEFAULT '{}',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        """

    cur.execute(create_sql)
    conn.commit()
    print("✓ 'users' table created or already exists.")

    # Check table columns
    if db_type == "postgresql":
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'users';
        """)
        cols = cur.fetchall()
        print("Columns in users table:")
        for col in cols:
            print(f"  - {col[0]} ({col[1]})")
    else:
        cur.execute("PRAGMA table_info(users);")
        cols = cur.fetchall()
        print("Columns in users table:")
        for col in cols:
            print(f"  - {col[1]} ({col[2]})")

    conn.close()

if __name__ == "__main__":
    setup_users_table()
