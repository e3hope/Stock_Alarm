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

def createBookmark(id, keyword):
    
    # 관심종목 여부 확인
    try:
        sql = 'INSERT INTO bookmark (name, chat_id) VALUES (%s, %s)'
        inc.cursor.execute(sql, (keyword, str(id)))
        inc.conn.commit()
        result = True
    
    except:
        inc.conn.rollback()
        result = False
    
    return result

def readBookmark(id):
    sql = 'SELECT name FROM bookmark WHERE chat_id = %s'
    inc.cursor.execute(sql, [str(id)])
    result = [item[0] for item in inc.cursor.fetchall()]
    return result

def deleteBookmark(id, keyword):

    # 관심종목 여부 확인
    try:
        sql = 'DELETE FROM bookmark WHERE chat_id = %s AND name = %s'
        inc.cursor.execute(sql, (str(id), keyword))
        inc.conn.commit()
        result = True

    except:
        inc.conn.rollback()
        result = False
    
    return result

def createLimit(id, keyword, table, price):
    try:
        sql = 'INSERT INTO ' + table + ' (name, chat_id, price) VALUES (%s, %s, %s) ON CONFLICT (chat_id, name) DO UPDATE SET name = %s, price = %s'
        inc.cursor.execute(sql, (keyword, str(id), price, keyword, price))
        inc.conn.commit()
        result = True

    except:
        inc.conn.rollback()
        result = False
    
    return result

def readLimit(id, keyword):
    try:
        result = {}
        for table in ['low','high']:
            sql = 'SELECT price FROM ' + table + ' WHERE chat_id = %s AND name = %s'
            inc.cursor.execute(sql, (str(id), keyword))
            temp = inc.cursor.fetchone()
            result[table] = temp[0]
    except:
        result = None
    
    return result

def deleteLimit(id, keyword):
    for table in ['low','high']:
        try:
            sql = 'DELETE FROM ' + table + ' WHERE chat_id = %s AND name = %s '
            inc.cursor.execute(sql, (str(id), keyword))
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