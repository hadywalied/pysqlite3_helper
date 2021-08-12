from src.Database.setup.helper import Helper, scrub


class EthernetHelper(Helper):
    '''a subclass of the Helper Class to handle the creation of the Ethernet specific Tables
        to create any table, simply dublicate the  create_sa_table and change the table name and fields'''

    def __init__(self):
        '''create a database file for the ethernet tables in eth.db '''
        super(EthernetHelper, self).__init__('src/Database/Ethernet/eth.db')
        # self.create_tables()

    def create_tables(self):
        '''creates the tables of the ethernet database'''
        try:
            self.create_sa_table()
            self.db.commit()
        except:
            print('one or more tables already exists')

    def create_sa_table(self):
        '''create the Standalone Table with the proper fields'''
        self.cur.execute("DROP TABLE IF EXISTS SA")
        self.cur.execute('''CREATE TABLE SA (speed text unique, dc_memory_value integer,tolerance integer)''')

    def create_mpg_table(self):
        '''create the MPG Table with the proper fields'''
        self.cur.execute("DROP TABLE IF EXISTS MPG")
        self.cur.execute('''CREATE TABLE MPG (speed text unique, dc_memory_value integer,tolerance integer)''')

    def drop_table(self, table_name):
        '''to remove a table in the db'''
        query = 'DROP TABLE IF EXISTS {table}'.format(table=scrub(table_name))
        self.cur.execute(query)
        self.db.commit()
