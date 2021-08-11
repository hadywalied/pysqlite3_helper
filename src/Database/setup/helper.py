import sqlite3


def scrub(name):
    return ''.join(ch for ch in name if ch.isalnum())


class Helper(object):
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
        '''insert into the table {table_name} the values listed in the tuple {values}'''
        query = 'insert into {table}'.format(table=scrub(table_name))
        self.cur.execute('''{query} values {values}'''.format(query=query, values=tuple(values)))
        self.db.commit()

    def update_value_in_table(self, table_name: str, lookup_col, lookup_value, intended_col, new_value):
        '''update values in {intended_col, new_value} of the table {table_name} according to
            the {lookup_col, lookup_value} which are the primary identifiers of the table '''

        query = 'update {table}'.format(table=scrub(table_name))
        values = (intended_col, new_value, lookup_col, lookup_value)
        self.cur.execute('''{query} set ? = ? where ? = ? '''.format(query=query), values)
        self.db.commit()

    def get_all_elements(self, table_name: str):
        '''get all the elements of the table {table_name}'''

        query = 'select * from {table}'.format(table=scrub(table_name))
        elements = list(self.cur.execute(query))
        self.db.commit()
        return elements

    def get_elements_subject_to_col(self, table_name: str, column: str, value: str):
        '''get all the elements of the table {table_name} subject to the {column, value}'''

        query = "select * from {table} where {col} == '{value}' ".format(table=scrub(table_name), col=scrub(column),
                                                                         value=scrub(value))
        elements = list(self.cur.execute(query))
        self.db.commit()
        return elements

    def remove_from_table_with_column_col(self, table_name: str, column: str, value: str):
        '''remove elements of the table {table_name} subject to the {column, value}'''
        query = 'delete from {table}'.format(table=scrub(table_name))
        values = (column, value)
        self.cur.execute('''{query} where ? like ?'''.format(query=query), values)
        self.db.commit()

    def empty_table(self, table_name: str):
        '''empty the table {table_name} from all the values'''
        query = 'delete from {table}'.format(table=scrub(table_name))
        self.cur.execute(query)
        self.db.commit()

    def __del__(self):
        '''close the connection to the database'''
        self.db.close()
