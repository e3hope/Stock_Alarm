import inc
import stock

# 종가 불러오기
data = stock.close()

# 유저별 관심종목 보내기
for x,y in data.items():
    text = ''
    for z in y:
        for k,v in z.items():
            temp = k + '의 종가: ' + str(format(v, ',')) + '원\n'
        text = temp + text
    inc.bot.sendMessage(chat_id = x, text = text)

inc.close()