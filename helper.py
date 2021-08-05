import sqlite3


def scrub(name):
    return ''.join(ch for ch in name if ch.isalnum())


class Helper:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.db = sqlite3.connect(db_path)
        self.cur = self.db.cursor()

    def insert_into_table(self, table_name: str, values: tuple):
        query = f'insert into {scrub(table_name)}'
        self.cur.execute(f'''{query} values {tuple(values)}''')
        self.db.commit()

    def update_value_in_table(self, table_name: str, lookup_col, lookup_value, intended_col, new_value):
        query = f'update {scrub(table_name)}'
        values = (intended_col, new_value, lookup_col, lookup_value)
        self.cur.execute(f'''{query} set ? = ? where ? = ? ''', values)
        self.db.commit()

    def get_all_elements(self, table_name: str):
        query = f'select * from {scrub(table_name)}'
        elements = list(self.cur.execute(f'''{query}'''))
        self.db.commit()
        return elements

    def get_elements_subject_to_col(self, table_name: str, col: str, value: str):
        query = f"select * from {scrub(table_name)} where {scrub(col)} == '{scrub(value)}' "
        elements = list(self.cur.execute(f"{query}"))
        self.db.commit()
        return elements

    def remove_from_table_with_column_col(self, table_name: str, col: str, value: str):
        query = f'delete from {scrub(table_name)}'
        values = (col, value)
        self.cur.execute(f'''{query} where ? like ?''', values)
        self.db.commit()

    def empty_table(self, table_name: str):
        query = f'delete from {scrub(table_name)}'
        self.cur.execute(f'''{query}''')
        self.db.commit()

    def __del__(self):
        self.db.close()
