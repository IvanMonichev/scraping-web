import os
import sqlite3


class Database:
    def __init__(self, db_name='data/articles.db'):
        os.makedirs(os.path.dirname(db_name), exist_ok=True)
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('DROP TABLE IF EXISTS articles')
        self.cursor.execute('''
            CREATE TABLE articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                link TEXT NOT NULL,
                description TEXT,
                datetime_published TEXT,
                author TEXT,
                author_profile_url TEXT
            )
        ''')
        self.conn.commit()
        print('Table articles has been created.')

    def insert_articles(self, articles):
        # Вставляем записи из articles
        for article in articles:
            self.cursor.execute('''
                INSERT INTO articles (title, link, description, datetime_published, author, author_profile_url)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                article['title'],
                article['link'],
                article['description'],
                article['datetime_published'],
                article['author']['author'],
                article['author']['author_profile_url']
            ))
        self.conn.commit()

    def close(self):
        self.conn.close()
