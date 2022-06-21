import telegram
import psycopg2
import re
import inc

#bot을 선언
bot = telegram.Bot(token = inc.set['Telegram']['token'])

# # 디비 연결
# conn = psycopg2.connect(host='localhost', user='e3hope', password='ds64079376*', db='SN', charset='utf8')
# cursor = conn.cursor()
