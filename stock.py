import FinanceDataReader as fdr
import datetime
import inc

# 종목 데이터
def info(keyword,period):

    # 코드 구하기
    code = getCode(keyword)
    
    # 예외처리
    if code is None:
        return '상장하지 않은 회사입니다.'
    
    
    
    # 장전 예외처리
    if datetime.datetime.now().hour < 9:

        date = datetime.datetime.now() - datetime.timedelta(days = period + 1)
        df = fdr.DataReader(code, date, datetime.datetime.now() - datetime.timedelta(days = 1))[['Close','Change']]

    else:

        date = datetime.datetime.now() - datetime.timedelta(days = period)
        df = fdr.DataReader(code, date)[['Close','Change']]

    # 날짜변수 문자열 타입 변환
    df.index = df.index.strftime('%Y-%m-%d')

    # 총 합계 변수
    start = df['Close'].head(1).transpose().to_list()[0]
    end = df['Close'].tail(1).transpose().to_list()[0]
    sum = round((end - start) / start * 100, 2)

    # 퍼센트 변환
    df['Change'] = round(df['Change'] * 100, 2).apply(str)

    data = df.transpose().to_dict()
    
    text = str(keyword) + '의 ' + str(period) + '일간 변동률\n'
    for x,y in data.items():
        temp = str(x) + '\n' + ( '현재가: ' if str(datetime.datetime.now().date()) == x else '종가: ' ) + str(format(y['Close'], ',')) + '원 ' + ( '↑' if float(y['Change']) >= 0 else '↓' ) + y['Change']
        
        if period != 1:
            temp =  temp + '%\n'
        text = text + temp

    if period == 1:
        return text + '%'
    else:
        return text + str(period) + '일간의 합계: ' + ( '↑' if int(sum) >= 0 else '↓' ) + str(sum) + '%\n'

def getClose():

    # code 구하기
    sql = 'SELECT b.chat_id, b."name", s.code FROM bookmark AS b INNER JOIN stock AS s ON(b.name  = s.name)'
    inc.cursor.execute(sql)
    result = inc.cursor.fetchall()
    chat_id,name,code = zip(*result)

    # 종목 종가 추출
    Close = []
    for i in range(len(code)):
        temp = fdr.DataReader(code[i], datetime.datetime.now() - datetime.timedelta(days = 1))[['Close','Change']]
        temp['Change'] = round(temp['Change'] * 100, 2).apply(str)
        Close.append(list(temp.transpose().to_dict().values()))

    data = {}   
    for i in range(len(chat_id)):
        if chat_id[i] in data:
            data[chat_id[i]].append({name[i]:Close[i]})
        else: 
            data[chat_id[i]] = [{name[i]:Close[i]}]
    
    return data

def getLow():
    sql = 'SELECT l.idx, l.chat_id, l."name", l.price, s.code FROM low AS l INNER JOIN stock AS s ON(l.name = s.name)'
    inc.cursor.execute(sql)
    result = inc.cursor.fetchall()
    idx,chat_id,name,price,code = zip(*result)
    
    # 종목 종가 추출
    Close = []
    for i in range(len(code)):
        temp = fdr.DataReader(code[i], datetime.datetime.now() - datetime.timedelta(days = 1))['Close']
        Close.append(list(temp.transpose().to_dict().values())[0])
    
    data = {}
    delete = []
    for i in range(len(chat_id)):
        if int(price[i]) >= Close[i]:
            if chat_id[i] in data:
                data[chat_id[i]].append({name[i]:price[i]})
            else: 
                data[chat_id[i]] = [{name[i]:price[i]}]
            delete.append(idx[i])

    if delete:
        try:
            sql = 'DELETE FROM low WHERE idx IN %s'
            inc.cursor.execute(sql, (tuple(delete),))
            inc.conn.commit()

        except:
            inc.conn.rollback()
    
    return data

def getHigh():
    sql = 'SELECT l.idx, l.chat_id, l."name", l.price, s.code FROM high AS l INNER JOIN stock AS s ON(l.name = s.name)'
    inc.cursor.execute(sql)
    result = inc.cursor.fetchall()
    idx,chat_id,name,price,code = zip(*result)
    
    # 종목 종가 추출
    Close = []
    for i in range(len(code)):
        temp = fdr.DataReader(code[i], datetime.datetime.now() - datetime.timedelta(days = 1))['Close']
        Close.append(list(temp.transpose().to_dict().values())[0])
    
    data = {}
    delete = [] 
    for i in range(len(chat_id)):
        if int(price[i]) <= Close[i]:
            if chat_id[i] in data:
                data[chat_id[i]].append({name[i]:price[i]})
            else: 
                data[chat_id[i]] = [{name[i]:price[i]}]
            delete.append(idx[i])

    if delete:
        try:
            sql = 'DELETE FROM high WHERE idx IN %s'
            inc.cursor.execute(sql, (tuple(delete),))
            inc.conn.commit()

        except:
            inc.conn.rollback()
    
    return data

def getBookmark(id):

    try:
        sql = 'SELECT b."name", s.code FROM bookmark AS b INNER JOIN stock AS s ON(b.name  = s.name) WHERE b.chat_id = %s'
        inc.cursor.execute(sql,[str(id)])
        result = inc.cursor.fetchall()
        name,code = zip(*result)

        # 종목 종가 추출
        Close = []
        for i in range(len(code)):

            # 장전 예외처리
            if datetime.datetime.now().hour < 9:
                temp = fdr.DataReader(code[i], datetime.datetime.now() - datetime.timedelta(days = 2))['Close']
                Close.append(list(temp.transpose().to_dict().values())[0])
            
            else:
                temp = fdr.DataReader(code[i], datetime.datetime.now() - datetime.timedelta(days = 1))['Close']
                Close.append(list(temp.transpose().to_dict().values())[0])


        data = {}   
        for i in range(len(name)):
                data[name[i]] = Close[i]

    except:
        data = None

    return data

# 현재가격 구하기
def now(keyword):
    
    # 코드 구하기
    code = getCode(keyword)

    if code is not None:
        try:
            # 장전 예외처리
            if datetime.datetime.now().hour < 9:
                temp = fdr.DataReader(code, datetime.datetime.now() - datetime.timedelta(days = 2))['Close']
                data = list(temp.transpose().to_dict().values())[0]

            else:
                temp = fdr.DataReader(code, datetime.datetime.now() - datetime.timedelta(days = 1))['Close']
                data = list(temp.transpose().to_dict().values())[0]
        except:
            data = None

    else:
        data = None

    return data

# 종목 코드
def getCode(keyword):
    
    # 디비에서 종목코드 가져오기
    try:
        lastupdatesql = 'SELECT code FROM stock WHERE name = %s'
        inc.cursor.execute(lastupdatesql,[keyword])
        code = inc.cursor.fetchone()[0]

    # 없는경우 finace api로 종목코드 구하기
    # except TypeError:
    #     try:
    #         df_krx = fdr.StockListing('KRX')
    #         code = df_krx.where(df_krx['Name'] == keyword).dropna()['Symbol'].values[0]
    #     except:
    #         return None

    # 둘다없으면 리턴 
    except:
        return None

    return code