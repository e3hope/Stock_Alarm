import FinanceDataReader as fdr
import datetime
# from . import inc

# 종목명 받아오기
keyword = '하이브'
date = None

# 종목코드 구하기
df_krx = fdr.StockListing('KRX')
code = df_krx.where(df_krx['Name'] == keyword).dropna()['Symbol'].values[0]

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
print(data)