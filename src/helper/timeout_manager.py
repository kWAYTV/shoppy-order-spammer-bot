import time
import sqlite3

class TimeoutManager:
    def __init__(self):
        self.connection = sqlite3.connect('timeout_db.sqlite')
        self.create_table()

    def __del__(self):
        self.connection.close()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS timeout_db (
                user_id TEXT PRIMARY KEY,
                timeout REAL
            );
        ''')
        self.connection.commit()

    def add_user(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO timeout_db(user_id, timeout) VALUES(?, ?)", (user_id, time.time()))
        self.connection.commit()

    def remove_user(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM timeout_db WHERE user_id = ?", (user_id,))
        self.connection.commit()

    def is_user_in_timeout(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM timeout_db WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        if user is None:
            return False, None

        elapsed_time = time.time() - user[1]  # Access the second element of the tuple
        if elapsed_time < 1800:
            return True, 1800 - elapsed_time
        else:
            self.remove_user(user_id)
            return False, None
