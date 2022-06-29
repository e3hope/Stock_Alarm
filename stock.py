import FinanceDataReader as fdr
import datetime
import inc

# 종목 데이터
def info(keyword,period):

    # 코드 구하기
    code = getcode(keyword)
    
    # 예외처리
    if code is None:
        return '상장하지 않은 회사입니다.'
    
    date = datetime.datetime.now() - datetime.timedelta(days = period + 2)

    # 해당종목 일주일치 데이터 및 합계 출력
    df = fdr.DataReader(code, date)[['Close','Change']]

    # 날짜변수 문자열 타입 변환
    df.index = df.index.strftime('%Y-%m-%d')

    # 총 합계 변수
    sum = str(round(df['Change'].sum() * 100, 2)) + '%'

    # 퍼센트 변환
    df['Change'] = round(df['Change'] * 100, 2).apply(str)

    data = df.transpose().to_dict()
    # data['Sum'] = sum

    text = str(keyword) + '의 ' + str(period) + '일간 변동률\n'
    for x,y in data.items():
        temp = str(x) + '\n 종가: ' + str(format(y['Close'], ',')) + '원 ' + ( '↑' if float(y['Change']) >= 0 else '↓' ) + y['Change'] + '%\n'
        text = text + temp
    return text + str(period) + '일간의 합계: ' + str(sum)

def getclose():

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

def getlow():
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
        if int(price[i]) <= Close[i]:
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

def gethigh():
    sql = 'SELECT l.idx, l.chat_id, l."name", l.price, s.code FROM high AS l INNER JOIN stock AS s ON(l.name = s.name)'
    inc.cursor.execute(sql)
    result = inc.cursor.fetchall()
    chat_id,name,price,code = zip(*result)
    
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

    if delete:
        try:
            sql = 'DELETE FROM high WHERE idx IN %s'
            inc.cursor.execute(sql, (tuple(delete),))
            inc.conn.commit()

        except:
            inc.conn.rollback()
    
    return data

# 현재가격 구하기
def now(keyword):
    
    # 코드 구하기
    code = getcode(keyword)

    try:
        temp = fdr.DataReader(code, datetime.datetime.now() - datetime.timedelta(days = 1))['Close']
        data = list(temp.transpose().to_dict().values())[0]
    except:
        return None
    
    return data

# 종목 코드
def getcode(keyword):
    
    # 디비에서 종목코드 가져오기
    try:
        lastupdatesql = 'SELECT code FROM stock WHERE name = %s'
        inc.cursor.execute(lastupdatesql,[keyword])
        code = inc.cursor.fetchone()[0]

    # 없는경우 finace api로 종목코드 구하기
    except TypeError:
        try:
            df_krx = fdr.StockListing('KRX')
            code = df_krx.where(df_krx['Name'] == keyword).dropna()['Symbol'].values[0]
        except:
            return None

    # 둘다없으면 리턴 
    except:
        return None

    return code