import FinanceDataReader as fdr
import matplotlib.pyplot as plt
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
    
    return data, sum
    # ({'2022-07-22': {'Close': 6440, 'Change': '-9.55'}, '2022-07-25': {'Close': 6350, 'Change': '-1.4'}}, -1.4)

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
        Close.append(list(temp.transpose().to_dict().values())[0])

    data = {}   
    
    for i in range(len(chat_id)):
        if chat_id[i] in data:
            data[chat_id[i]][name[i]] = Close[i]
        else: 
            data[chat_id[i]] = {name[i]:Close[i]}
    
    return data
    # {'942186215': {'파인디앤씨': {'Close': 1650, 'Change': '1.54'}, '이트론': {'Close': 190, 'Change': '-1.04'}}, '5510686398': {'삼성전자': {'Close': 61400, 'Change': '0.16'}}

def getLow():
    sql = 'SELECT l.idx, l.chat_id, l."name", l.price, s.code FROM low AS l INNER JOIN stock AS s ON(l.name = s.name)'
    inc.cursor.execute(sql)
    result = inc.cursor.fetchall()
    idx,chat_id,name,price,code = zip(*result)
    
    # 종목 종가 추출
    Close = []
    for i in range(len(code)):
        temp = getStock(code[i])
        Close.append(list(temp.transpose().to_dict().values())[0])
    
    data = {}
    delete = []
    for i in range(len(chat_id)):
        if int(price[i]) >= Close[i]:
            if chat_id[i] in data:
                data[chat_id[i]][name[i]] = price[i]
            else: 
                data[chat_id[i]] = {name[i]:price[i]}
            delete.append(idx[i])

    if delete:
        try:
            sql = 'DELETE FROM low WHERE idx IN %s'
            inc.cursor.execute(sql, (tuple(delete),))
            inc.conn.commit()

        except:
            inc.conn.rollback()
    
    return data
    # {'1119827172': {'세종메디칼': '6000'}}

def getHigh():
    sql = 'SELECT l.idx, l.chat_id, l."name", l.price, s.code FROM high AS l INNER JOIN stock AS s ON(l.name = s.name)'
    inc.cursor.execute(sql)
    result = inc.cursor.fetchall()
    idx,chat_id,name,price,code = zip(*result)
    
    # 종목 종가 추출
    Close = []
    for i in range(len(code)):
        temp = getStock(code[i])
        Close.append(list(temp.transpose().to_dict().values())[0])
    
    data = {}
    delete = [] 
    for i in range(len(chat_id)):
        if int(price[i]) <= Close[i]:
            if chat_id[i] in data:
                data[chat_id[i]][name[i]] = price[i]
            else: 
                data[chat_id[i]] = {name[i]:price[i]}
            delete.append(idx[i])

    if delete:
        try:
            sql = 'DELETE FROM high WHERE idx IN %s'
            inc.cursor.execute(sql, (tuple(delete),))
            inc.conn.commit()

        except:
            inc.conn.rollback()
    
    return data
    # {'1119827172': {'세종메디칼': '6000'}}

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

                # 월요일인 경우
                if datetime.datetime.today().weekday() == 0:
                    temp = getStock(code[i],4)
                temp = getStock(code[i],2)

            else:
                temp = getStock(code[i])
            Close.append(list(temp.transpose().to_dict().values())[0])

        data = {}   
        for i in range(len(name)):
                data[name[i]] = Close[i]

    except:
        data = None

    return data
    # {'룽투코리아': 5080, '세종메디칼': 6270, '펄어비스': 53000}

# 현재가격 구하기
def now(keyword):
    
    # 코드 구하기
    code = getCode(keyword)

    if code is not None:
        try:
            # 장전 예외처리
            if datetime.datetime.now().hour < 9:
                
                # 월요일인 경우
                if datetime.datetime.today().weekday() == 0:
                    temp = getStock(code,4)
                temp = getStock(code,2)

            else:
                temp = getStock(code)

            data = list(temp.transpose().to_dict().values())[0]
        except:
            data = None

    else:
        data = None

    return data
    # 6310

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
    # 258830

# 주식 가격
def getStock(code,period = 1):
    data = fdr.DataReader(code, datetime.datetime.now() - datetime.timedelta(days = period))['Close']

    return data
    # Date
    # 2022-07-22    6440
    # 2022-07-25    6320

# 주식차트
def getImage(code,period = 7):

    if period < 7:
        return None
    
    data = getStock(code,period)
    data.plot()

    filepath = inc.environment[inc.branch] + 'Image/'
    filename = str(datetime.datetime.now()) + '.jpg'
    plt.savefig(filepath + filename)

    return filepath + filename