import sqlite3 
import pprint 
pp = pprint.PrettyPrinter(indent = 1, width = 80, compact = False)
conn = sqlite3.connect('Lab24/BD_Shop.sqlite') 
c = conn.cursor() 
c.execute('''PRAGMA foreign_keys = 1''')

c.execute("DROP VIEW IF EXISTS prices_last")
c.execute("DROP VIEW IF EXISTS vendors_incoming")
c.execute("DROP VIEW IF EXISTS vendors_incoming_magazine")

c.execute('''CREATE VIEW IF NOT EXISTS prices_last AS
          SELECT id_product, date_price_changes, price
          FROM prices AS a
          WHERE date_price_changes = (SELECT MAX(date_price_changes)
                FROM prices
                WHERE a.id_product = prices.id_product)''')
conn.commit()

c.execute('''CREATE VIEW IF NOT EXISTS vendors_incoming AS
          SELECT v.name, i.date_incoming 
          FROM vendors AS v
          JOIN incoming AS i ON v.id_vendor = i.id_vendor''')
conn.commit()

c.execute('''CREATE VIEW IF NOT EXISTS vendors_incoming_magazine AS
          SELECT * FROM vendors
          JOIN incoming ON 
          JOIN 

          name FROM vendors 
          date_incoming FROM incoming 
          magazine_incoming




          FROM vendors AS v
          JOIN incoming AS i ON v.id_vendor = i.id_vendor''')
conn.commit()

c.execute('''select * from prices_last''')
pp.pprint(c.fetchall())
c.execute('''select * from vendors_incoming''')
pp.pprint(c.fetchall())
c.execute('''select * from vendors_incoming_magazine''')
pp.pprint(c.fetchall())
conn.close()