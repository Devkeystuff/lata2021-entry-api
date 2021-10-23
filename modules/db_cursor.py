import os
import psycopg2


class DbCursor(object):
    def __init__(self):
        super().__init__()
        self.conn = psycopg2.connect(
            f'dbname={os.environ["DB_DATABASE"]} '
            f'user={os.environ["DB_USER"]} '
            f'host={os.environ["DB_HOST"]} '
            f'password={os.environ["DB_PASS"]} '
        )
        self.cursor = None

    def __enter__(self):
        self.conn.__enter__()
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.__exit__(self, exc_type, exc_val, exc_tb)
        self.conn.__exit__(exc_type, exc_val, exc_tb)
