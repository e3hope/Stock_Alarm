import FinanceDataReader as fdr
import datetime
import inc

# 종목 데이터
def stock_data(keyword, date = None):

    # 코드 구하기
    code = stock_code(keyword)
    
    # 예외처리
    if code is None:
        return '상장하지 않은 회사입니다.'
    
    # 날짜 구하기 ( 일주일 전 )
    if date is None:
        date = datetime.datetime.now() - datetime.timedelta(days = 10)

    # 해당종목 일주일치 데이터 및 합계 출력
    df = fdr.DataReader(code, date)[['Close','Change']]

    # 날짜변수 문자열 타입 변환
    df.index = df.index.strftime('%Y-%m-%d')

    # 총 합계 변수
    sum = str(round(df['Change'].sum() * 100, 2)) + '%'

    # 퍼센트 변환
    df['Change'] = round(df['Change'] * 100, 2).apply(str) + '%'

    data = df.transpose().to_dict()
    data['Sum'] = sum
    return data

# 종목 코드
def stock_code(keyword):
    
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