import sqlite3 as sql


class Cursor:
    def __init__(self, path: str):
        self.db = sql.connect(path, check_same_thread=False)
        self.cur = self.db.cursor()

    def select(self,
               table: str,
               cols: [tuple | list | str],
               distinct: bool = False,
               filter_cols: dict = {}):

        req = """SELECT """
        if distinct:
            req += """DISTINCT """

        if isinstance(cols, str):
            req += cols + ' '
        else:
            req += ', '.join(cols) + ' '
        req += f"""FROM {table} """

        if filter_cols:
            s = ' AND '.join(map(lambda x: f'{x} = ?', filter_cols.keys()))
            req += f"""WHERE {s}"""
        return self.cur.execute(req, tuple(filter_cols.values()))

    def insert(self,
               table: str,
               values: tuple):

        self.cur.execute(f"INSERT INTO {table} VALUES({', '.join(['?'] * len(values))})", values)
        self.db.commit()

    def update(self,
               table: str,
               set_cols: dict,
               filter_cols: dict):

        set_s = ', '.join(map(lambda x: f'{x} = ?', set_cols.keys()))
        filter_s = ', '.join(map(lambda x: f'{x} = ?', filter_cols.keys()))

        self.cur.execute(f"UPDATE {table} SET {set_s} WHERE {filter_s}", tuple(set_cols) + tuple(filter_cols))
        self.db.commit()

    def close(self):
        self.db.close()
