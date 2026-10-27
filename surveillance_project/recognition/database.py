import sqlite3, datetime

DB_FILE = 'surveillance.db'

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                person_id INTEGER,
                timestamp TEXT,
                camera_id TEXT,
                classification TEXT,
                confidence REAL,
                image_path TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS people (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE
            )
        ''')

def log_event(person_id, camera_id, classification, confidence, image_path):
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            'INSERT INTO events VALUES (NULL,?,?,?,?,?,?)',
            (person_id, ts, camera_id, classification, confidence, image_path)
        )

def add_person(name):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute('INSERT INTO people (name) VALUES (?)', (name,))
            conn.commit()
            return conn.execute('SELECT id FROM people WHERE name = ?', (name,)).fetchone()[0]
    except sqlite3.IntegrityError:
        with sqlite3.connect(DB_FILE) as conn:
            return conn.execute('SELECT id FROM people WHERE name = ?', (name,)).fetchone()[0]
