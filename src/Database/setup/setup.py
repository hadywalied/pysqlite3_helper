from src.Database.setup.Ethernet.ethrenet_helper import EthernetHelper

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
    helper.create_tables()
    # helper.cur.execute('''insert into SA values ('CGMII',1,2,3,4,5)''')
    # helper.cur.execute('''insert into SA values ('XGMII',1,2,23,421,15)''')
    # helper.cur.execute('''insert into SA values ('CGMII',12,20,300,40,23)''')
    # helper.db.commit()
    items = [
        ('CGMII', 1, 2),
        ('XGMII', 1, 2),
        # ('CGMII', 12, 20)
    ]
    for item in items:
        helper.insert_into_table('SA', item)

    # for row in helper.cur.execute('select * from SA'):
    #     print(row)
    print(helper.get_all_elements('SA'))
    print(helper.get_elements_subject_to_col('SA', column='speed', value='CGMII')[0]['tolerance'])
    del helper
