import inc
import stock

# 종가 불러오기
data = stock.getClose()

# 유저별 관심종목 종가 보내기
for x,y in data.items():
    text = ''
    for k,v in y.items():
        temp = k + '의 종가: ' + str(format(v['Close'], ',')) + '원' + ( '↑' if float(v['Change']) >= 0 else '↓' ) + v['Change'] + '%\n'
        text = temp + text
    inc.bot.sendMessage(chat_id = x, text = text)

inc.close()