from src.Database.setup.helper import Helper, scrub


class FiveGHelper(Helper):
    '''a subclass of the Helper Class to handle the creation of the 5G specific Tables
        to create any table, simply dublicate the  create_sa_table and change the table name and fields'''

    def __init__(self):
        '''create a database file for the ethernet tables in ethg.db '''
        super(FiveGHelper, self).__init__('./FiveG/FiveG.db')
        # self.create_tables()

    def create_tables(self):
        '''creates the tables of the 5G database'''
        self.create_sa_table()
        # self.cur.execute('''CREATE TABLE MPG ()''')
        # self.cur.execute('''CREATE TABLE vFlex ()''')
        self.db.commit()

    def create_sa_table(self):
        '''create the Standalone Table with the proper fields'''
        self.cur.execute("DROP TABLE IF EXISTS SA")
        self.cur.execute('''CREATE TABLE SA (id integer distinct increment, dc_memory_value integer,memory_per_bbu integer, memory_per_ru integer, 
         memory_for_streaming integer, memory_per_configure integer)''')

    def drop_table(self, table_name):
        '''to remove a table in the db'''
        query = f'DROP TABLE IF EXISTS {scrub(table_name)}'
        self.cur.execute(query)
        self.db.commit()