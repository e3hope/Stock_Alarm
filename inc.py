import telegram
import psycopg2
import json
import platform

# setting값 연동
if platform.platform() == 'Linux-5.8.0-44-lowlatency-x86_64-with-glibc2.29':
    set_path = './setting.json'
else:
    set_path = '/home/Stock_Alarm/Stock_Alarm/setting.json'
with open(set_path, 'r', encoding = 'utf8') as f:
    set = json.load(f)

# 디비 연결
conn = psycopg2.connect(
    host = set['DB']['host'], 
    port = set['DB']['port'], 
    user = set['DB']['user'], 
    password = set['DB']['password'], 
    dbname = set['DB']['db']
)
cursor = conn.cursor()

#bot을 선언
bot = telegram.Bot(token = set['Telegram']['token'])

# 마지막 업데이트목록
def lastupdate():
    sql = 'SELECT update_id FROM lastupdate'
    cursor.execute(sql)
    offset = cursor.fetchone()
    return offset[0]

def close():
    conn.close()