import sqlite3
from datetime import datetime

DB_NAME = 'usage.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage (
            user_id INTEGER,
            search_type TEXT,
            last_used DATE,
            PRIMARY KEY (user_id, search_type)
        )
    ''')
    conn.commit()
    conn.close()

def can_use_search(user_id: int, search_type: str) -> bool:
    """Проверяет, можно ли пользователю использовать поиск сегодня."""
    today = datetime.now().date()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT last_used FROM usage WHERE user_id=? AND search_type=?', (user_id, search_type))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return True  # Никогда не использовал — можно
    last_used = datetime.strptime(row[0], '%Y-%m-%d').date()
    return last_used < today  # Можно, если последний раз был раньше сегодняшнего дня

def update_usage(user_id: int, search_type: str):
    """Обновляет дату использования поиска текущей датой."""
    today = datetime.now().date().isoformat()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usage (user_id, search_type, last_used)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, search_type) DO UPDATE SET last_used=excluded.last_used
    ''', (user_id, search_type, today))
    conn.commit()
    conn.close()

