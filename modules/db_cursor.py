import psycopg2
from modules.consts import DB_HOST, DB_PASS, DB_USER, DB_DATABASE


class DbCursor(object):
    def __init__(self):
        super().__init__()
        self.conn = psycopg2.connect(
            f'dbname={DB_DATABASE} '
            f'user={DB_USER} '
            f'host={DB_HOST} '
            f'password={DB_PASS} '
        )
        self.cursor = None

    def __enter__(self):
        self.conn.__enter__()
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.__exit__(self, exc_type, exc_val, exc_tb)
        self.conn.__exit__(exc_type, exc_val, exc_tb)
