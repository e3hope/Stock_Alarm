import inc
import FinanceDataReader as fdr

sql = 'TRUNCATE TABLE stock'
inc.cursor.execute(sql)

try:
    stocks = fdr.StockListing('KRX')[['Name','Symbol']]
    data = list(stocks.itertuples(index=False, name=None))
    stocks_str = b', '.join(inc.cursor.mogrify("(%s,%s)", x) for x in data)
    inc.cursor.execute(b"INSERT INTO stock VALUES " + stocks_str) 
    inc.conn.commit()
    
except:
    inc.conn.rollback()