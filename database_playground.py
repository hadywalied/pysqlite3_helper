from helper import Helper, scrub


class EthernetHelper(Helper):
    def __init__(self):
        super(EthernetHelper, self).__init__('ethernet.db')
        self.create_tables()

    def create_tables(self):
        try:
            self.create_sa_table()
            # self.cur.execute('''CREATE TABLE MPG ()''')
            # self.cur.execute('''CREATE TABLE vFlex ()''')
            self.db.commit()
        except:
            print('one or more tables already exists')

    def create_sa_table(self):
        self.cur.execute("DROP TABLE IF EXISTS SA")
        self.cur.execute('''CREATE TABLE SA (speed text, dc_memory_value integer,tolerance integer)''')

    def create_mpg_table(self):
        self.cur.execute("DROP TABLE IF EXISTS MPG")
        self.cur.execute('''CREATE TABLE MPG (speed text, dc_memory_value integer,tolerance integer)''')

    def drop_table(self, table_name):
        query = f'DROP TABLE IF EXISTS {scrub(table_name)}'
        self.cur.execute(f'''{query}''')
        self.db.commit()


class EthgHelper(Helper):
    def __init__(self):
        super(EthgHelper, self).__init__('ethg.db')
        self.create_tables()

    def create_tables(self):
        self.create_sa_table()
        # self.cur.execute('''CREATE TABLE MPG ()''')
        # self.cur.execute('''CREATE TABLE vFlex ()''')
        self.db.commit()

    def create_sa_table(self):
        self.cur.execute("DROP TABLE IF EXISTS SA")
        self.cur.execute('''CREATE TABLE SA (id integer distinct increment, dc_memory_value integer,memory_per_bbu integer, memory_per_ru integer, 
         memory_for_streaming integer, memory_per_configure integer)''')

    def drop_table(self, table_name):
        query = f'DROP TABLE IF EXISTS {scrub(table_name)}'
        self.cur.execute(f'''{query}''')
        self.db.commit()


if __name__ == "__main__":
    # con = sqlite3.connect('example.db')
    # cur = con.cursor()
    # cur.execute('''CREATE TABLE stocks
    #            (date text, trans text, symbol text, qty real, price real)''')
    # cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    # cur.execute("INSERT INTO stocks VALUES ('2006-01-06','BUY','RHAT',100,36.14)")
    # cur.execute("INSERT INTO stocks VALUES ('2006-01-07','BUY','RHAT',100,31.14)")
    # con.commit()
    # for row in cur.execute('SELECT * FROM stocks ORDER BY price'):
    #     print(row)
    # con.close()
    helper = EthernetHelper()
    # helper.create_tables()
    # helper.cur.execute('''insert into SA values ('CGMII',1,2,3,4,5)''')
    # helper.cur.execute('''insert into SA values ('XGMII',1,2,23,421,15)''')
    # helper.cur.execute('''insert into SA values ('CGMII',12,20,300,40,23)''')
    # helper.db.commit()
    items = [
        ('CGMII', 1, 2, 3, 4, 5),
        ('XGMII', 1, 2, 23, 421, 15),
        ('CGMII', 12, 20, 300, 40, 23)
    ]
    for item in items:
        helper.insert_into_table('SA', item)

    # for row in helper.cur.execute('select * from SA'):
    #     print(row)
    print(helper.get_all_elements('SA'))
    print(helper.get_elements_subject_to_col('SA', col='speed', value='CGMII'))
    del helper
