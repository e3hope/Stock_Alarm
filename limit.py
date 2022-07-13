import inc
import stock

# 종가 불러오기
low = stock.getLow()
high = stock.getHigh()

# 유저별 지정가 보내기
if low:
    for x,y in low.items():
        text = ''
        for z in y:
            for k,v in z.items():
                inc.bot.sendMessage(chat_id = x, text = k + '의 주가가 지정한 ' + str(format(int(v), ',')) + '원까지 떨어졌습니다.\n'
                                                        '해당 지정가는 자동으로 삭제됩니다.')


# 유저별 지정가 보내기
if high:
    for x,y in high.items():
        text = ''
        for z in y:
            for k,v in z.items():
                inc.bot.sendMessage(chat_id = x, text = k + '의 가격이 지정한 ' + str(format(int(v), ',')) + '원까지 올랐습니다.\n'
                                                        '해당 지정가는 자동으로 삭제됩니다.')

inc.close()