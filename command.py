import inc

def start(id, username, name):
    try:
        sql = 'INSERT INTO member (chat_id, id, name) VALUES (%s, %s, %s)'
        inc.cursor.execute(sql, (id, username, name))    
        inc.conn.commit()
        result = True
    except:
        inc.conn.rollback()
        result = False
    
    return result

def bookmark(id, keyword):

    # 관심종목 여부 확인
    try:
        bookmarksql = 'SELECT name FROM bookmark WHERE name = %s AND chat_id = %s'
        inc.cursor.execute(bookmarksql, (keyword, str(id)))
        bookmark = inc.cursor.fetchone()

        # 없으면 추가
        if bookmark is None:
            sql = 'INSERT INTO bookmark (name, chat_id) VALUES (%s, %s)'
            inc.cursor.execute(sql, (keyword, str(id)))
            inc.conn.commit()
            result = 'insert'

        # 있으면 삭제
        else:
            sql = 'DELETE FROM bookmark WHERE name = %s AND chat_id = %s'
            inc.cursor.execute(sql, (keyword, str(id)))
            inc.conn.commit()
            result = 'delete'

    except:
            inc.conn.rollback()
            result = 'error'
    
    return result

def low(id,keyword,price):
    try:
        sql = 'INSERT INTO low (name, chat_id, price) VALUES (%s, %s, %s) ON CONFLICT (chat_id) DO UPDATE SET name = %s, price = %s'
        inc.cursor.execute(sql, (keyword, str(id), price, keyword, price))
        inc.conn.commit()
        result = True

    except:
        inc.conn.rollback()
        result = False
    
    return result

def high(id,keyword,price):
    try:
        sql = 'INSERT INTO high (name, chat_id, price) VALUES (%s, %s, %s) ON CONFLICT (chat_id) DO UPDATE SET name = %s, price = %s'
        inc.cursor.execute(sql, (keyword, str(id), price, keyword, price))
        inc.conn.commit()
        result = True

    except:
        inc.conn.rollback()
        result = False
    
    return result

def limit_delete(id,keyword):
    for table in ['low','high']:
        try:
            sql = 'DELETE FROM ' + table + ' WHERE name = %s AND chat_id = %s'
            inc.cursor.execute(sql, (keyword, str(id)))
            inc.conn.commit()
            result = True

        except:
            inc.conn.rollback()
            result = False
    
    return result

def close(lastupdate):
    updatesql = 'UPDATE lastupdate SET update_id = %s'
    inc.cursor.execute(updatesql, [lastupdate])
    inc.conn.commit()