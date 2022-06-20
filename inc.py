import telegram
import psycopg2
import json

# setting값 연동
if set is None:
    set_path = './setting.json'
    with open(set_path) as f:
        set = json.load(f)

# 디비 설정
DB = set['DB']

# 디비 연결
conn = psycopg2.connect(
    host = DB['host'], 
    port = DB['port'], 
    user = DB['user'], 
    password = DB['password'], 
    db = DB['db'], 
    charset = DB['user']
)
cursor = conn.cursor()

# 텔레그램 설정
token = set['Telegram']['token']