import inc
import stock
import command

# 최종업데이트목록
offset = inc.lastupdate()
updates = inc.bot.getUpdates(offset = offset)

# 데이터 입력
for u in updates :
    
    # 남아있는 데이터 넘기기
    if u['update_id'] == offset :
        continue

    try:
        # 회원 입력
        if u.message.text == '/start' :
            result = command.start(u.message.chat.id, None if u.message.chat.username is None else u.message.chat.username, u.message.chat.last_name + u.message.chat.first_name)
            
            if result is True:
                inc.bot.sendMessage(chat_id = u.message.chat.id, text = '/help를 눌러 도움말을 확인하세요.')
            else:
                inc.bot.sendMessage(chat_id = u.message.chat.id, text = '이미 등록된 정보입니다.')

        # 관심 종목 입력
        elif u.message.text.startswith('@') :

            # 종목코드 추출
            keyword = u.message.text.replace('@', '')

            # 종목코드가 없는 경우
            if stock.getcode(keyword) is None:
                inc.bot.sendMessage(chat_id = u.message.chat.id, text = '상장되지않은 회사입니다.')
                continue

            result = command.bookmark(keyword,u.message.chat.id)

            if result == 'insert':
                inc.bot.sendMessage(chat_id = u.message.chat.id, text = '관심종목에"' + keyword + '"가 추가되었습니다.')
            elif result == 'delete':
                inc.bot.sendMessage(chat_id = u.message.chat.id, text = '관심종목에"' + keyword + '"가 삭제되었습니다.')
            else:
                inc.bot.sendMessage(chat_id = u.message.chat.id, text = '알수없는 오류로 인해 작동되지않았습니다. 관리자에게 문의주시기 바랍니다.')
        
        # 종목 일자별 변화율
        elif u.message.text.startswith('!') :
            
            # 종목 및 기간 추출
            temp = u.message.text.split()

            # 입력방식이 잘못된경우 리턴
            if len(temp) > 2:
                inc.bot.sendMessage(chat_id = u.message.chat.id, text = '입력방식이 잘못되었습니다.')
                continue

            keyword = temp[0].replace('!', '')
            period = int(temp[1]) if len(temp) == 2 else 7

            # 종목코드가 없는 경우
            if stock.getcode(keyword) is None:
                inc.bot.sendMessage(chat_id = u.message.chat.id, text = '상장되지않은 회사입니다.')
                continue
            
            inc.bot.sendMessage(chat_id = u.message.chat.id, text = stock.info(keyword,period))

        # 종목 지정가 지정
        elif u.message.text.startswith('$') :

            #  # 종목 및 기간 추출
            temp = u.message.text.split()

            # 입력방식이 잘못된경우 리턴
            if len(temp) > 3:
                inc.bot.sendMessage(chat_id = u.message.chat.id, text = '입력방식이 잘못되었습니다.')
                continue

            keyword = temp[0].replace('!', '')

        # 도움말
        elif u.message.text == '/help' :
            inc.bot.sendMessage(chat_id = u.message.chat.id, text='@{종목}을 입력하면 관심종목으로 지정됩니다. ex) @삼성전자\n'
                            '다시 한번입력 시 관심종목에서 삭제됩니다.\n'
                            '관심종목으로 지정시 15:35분에 종가 가격을 알람으로 보내드립니다~!\n'
                            '!{종목} {기간} 을 입력 시 기간별 변화율을 보여줍니다. ex) !삼성전자 7')
    except:
        continue

# 메세지 저장
if updates :
    command.close(updates[-1]['update_id'])
    
inc.close()