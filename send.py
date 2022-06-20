import telegram
import psycopg2
import re
import json

# inc 연동
set_path = './setting.json'
with open(set_path) as i:
    set = json.load(i)

print(set['DB'])

#bot을 선언
my_token = '1528268221:AAFJZkjDJT_Mw21OAnupbMrX4rSLgc0reJk'
bot = telegram.Bot(token = my_token)

# # 디비 연결
# conn = psycopg2.connect(host='localhost', user='e3hope', password='ds64079376*', db='SN', charset='utf8')
# cursor = conn.cursor()
