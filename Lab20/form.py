# Стандартный шаблон
import sqlite3 
import pprint 
pp = pprint.PrettyPrinter(indent=1, width=80, compact=False) 
conn = sqlite3.connect('Lab20/form.sqlite') 
c = conn.cursor() 

pp.pprint(c.fetchall())
conn.close() 
