import inc
import stock

# 종가 불러오기
data = stock.getClose()

# 유저별 관심종목 종가 보내기
for x,y in data.items():
    text = ''
    for z in y:
        for k,v in z.items():
            for vk,vv in v[0].items():
                if vk == 'Close':
                    temp = k + '의 종가: ' + str(format(vv, ',')) + '원'
                elif vk == 'Change':
                    temp = temp + ( '↑' if float(vv) >= 0 else '↓' ) + vv + '%\n'
        text = temp + text
    inc.bot.sendMessage(chat_id = x, text = text)

inc.close()