import sqlite3


def scrub(name):
    return ''.join(ch for ch in name if ch.isalnum())


class Helper:
    '''
    this is the sqlite3 database helper class, it contains helper functions to apply
    the CRUD (Create - Read - Update - Delete) operations to the database tables.
    '''

    def __init__(self, db_path='database.db'):
        '''initialize the database file path and connect to it'''
        self.db_path = db_path
        self.db = sqlite3.connect(db_path)
        self.cur = self.db.cursor()

    def insert_into_table(self, table_name: str, values: tuple):
        f'''insert into the table {table_name} the values listed in the tuple {values}'''
        query = f'insert into {scrub(table_name)}'
        self.cur.execute(f'''{query} values {tuple(values)}''')
        self.db.commit()

    def update_value_in_table(self, table_name: str, lookup_col, lookup_value, intended_col, new_value):
        f'''update values in {intended_col, new_value} of the table {table_name} according to 
            the {lookup_col, lookup_value} which are the primary identifiers of the table '''

        query = f'update {scrub(table_name)}'
        values = (intended_col, new_value, lookup_col, lookup_value)
        self.cur.execute(f'''{query} set ? = ? where ? = ? ''', values)
        self.db.commit()

    def get_all_elements(self, table_name: str):
        f'''get all the elements of the table {table_name}'''

        query = f'select * from {scrub(table_name)}'
        elements = list(self.cur.execute(f'''{query}'''))
        self.db.commit()
        return elements

    def get_elements_subject_to_col(self, table_name: str, column: str, value: str):
        f'''get all the elements of the table {table_name} subject to the {column, value}'''

        query = f"select * from {scrub(table_name)} where {scrub(column)} == '{scrub(value)}' "
        elements = list(self.cur.execute(f"{query}"))
        self.db.commit()
        return elements

    def remove_from_table_with_column_col(self, table_name: str, column: str, value: str):
        f'''remove elements of the table {table_name} subject to the {column, value}'''
        query = f'delete from {scrub(table_name)}'
        values = (column, value)
        self.cur.execute(f'''{query} where ? like ?''', values)
        self.db.commit()

    def empty_table(self, table_name: str):
        f'''empty the table {table_name} from all the values'''
        query = f'delete from {scrub(table_name)}'
        self.cur.execute(f'''{query}''')
        self.db.commit()

    def __del__(self):
        '''close the connection to the database'''
        self.db.close()
