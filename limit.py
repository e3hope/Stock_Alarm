import inc
import stock

# 종가 불러오기
low = stock.getlow()
high = stock.gethigh()

# 유저별 지정가 보내기
if low:
    for x,y in low.items():
        text = ''
        for z in y:
            for k,v in z.items():
                inc.bot.sendMessage(chat_id = x, text = k + '의 가격이 지정한 ' + v + '원에 도달했습니다.\n'
                                                        '해당 지정가는 자동으로 삭제됩니다.')


# 유저별 지정가 보내기
if high:
    for x,y in high.items():
        text = ''
        for z in y:
            for k,v in z.items():
                inc.bot.sendMessage(chat_id = x, text = k + '의 가격이 지정한 ' + v + '원에 도달했습니다.\n'
                                                        '해당 지정가는 자동으로 삭제됩니다.')

inc.close()