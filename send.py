import telegram
import psycopg2
import inc
import stock

#bot을 선언
bot = telegram.Bot(token = inc.set['Telegram']['token'])

# 데이터 확인
sql = 'SELECT chat_id, name FROM bookmark'
inc.cursor.execute(sql)
result = inc.cursor.fetchall()

# 유저별 키워드 기사 보내기
for u in result :
    bot.sendMessage(chat_id = u[0], text = stock.stock_data(u[1]))

inc.cursor.close