import telegram
import psycopg2
import json

# setting값 연동
set_path = 'setting.json'
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

# # 텔레그램 설정
# token = set['Telegram']['token']