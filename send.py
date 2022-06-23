import telegram
import psycopg2
import inc
import stock

#bot을 선언
bot = telegram.Bot(token = inc.set['Telegram']['token'])

# 종가 불러오기
data = stock.stock_close()

# 유저별 관심종목 보내기
for x,y in data.items():
    text = ''
    for z in y:
        for k,v in z.items():
            temp = k + '의 종가: ' + str(format(v, ',')) + '원\n'
        text = temp + text
    bot.sendMessage(chat_id = x, text = text)

inc.cursor.close