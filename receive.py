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

        # 도움말
        elif u.message.text == '/help' :
            inc.bot.sendMessage(chat_id = u.message.chat.id, text = '관심종목으로 지정시 15:35분에 종가 가격을 알람으로 보냅니다.\n'
                            '!조회 {종목} {기간} - 기간별 변화율을 보여줍니다. ex) !조회 삼성전자 7\n'
                            '!관심종목 조회 - 나의 관심종목 리스트를 조회합니다. ex) !관심종목 조회\n'
                            '!관심종목 추가 {종목} - 관심종목으로 지정됩니다.\n ex) !관심종목 추가 삼성전자\n'
                            '!관심종목 삭제 {종목} - 관심종목에서 삭제됩니다.\n ex) !관심종목 삭제 삼성전자\n'
                            '!지정가 조회 - 설정된 지정가를 보여줍니다. ex) !지정가 조회 삼성전자\n'
                            '!지정가 조회 {종목} - 개별종목의 설정된 지정가를 보여줍니다.\n ex) !지정가 조회 삼성전자\n'
                            '!지정가 추가 {종목} {가격} - 지정된 가격이 오면 알림을 보냅니다.\n ex) !지정가 추가 삼성전자 50000\n'
                            '!지정가 추가 {종목} {가격} - 재입력 시 지정된 가격을 수정해줍니다.\n ex) !지정가 추가 삼성전자 60000\n'
                            '!지정가 삭제 {종목} - 입력 시 지정가 알림을 삭제합니다.\n ex) !지정가 삭제 삼성전자')

        if u.message.text.startswith('!'):
            
            # 종목코드 추출
            temp = u.message.text.split()
            if len(temp) > 2:
                keyword = temp[2]

            # 관심종목
            if temp[0] == '!관심종목':
                
                # 관심종목 조회
                if temp[1] == '조회':
                    result = command.readBookmark(u.message.chat.id)
                    text = '\n'.join('⦁ ' + r for r in result)
                    inc.bot.sendMessage(chat_id = u.message.chat.id, text = u.message.chat.last_name + u.message.chat.first_name +'님의 관심종목\n' + text)

                # 관심종목 추가/삭제
                elif len(temp) == 3:               

                    # 종목코드가 없는 경우
                    if stock.getcode(keyword) is None:
                        inc.bot.sendMessage(chat_id = u.message.chat.id, text = '상장되지않은 회사입니다.')
                        continue

                    if temp[1] == '추가':
                        if command.createBookmark(u.message.chat.id,keyword):
                            inc.bot.sendMessage(chat_id = u.message.chat.id, text = '관심종목에"' + keyword + '"가 추가되었습니다.')
                        else:
                            inc.bot.sendMessage(chat_id = u.message.chat.id, text = '이미 추가된 관심종목입니다.')
                    
                    elif temp[1] == '삭제':
                        if command.deleteBookmark(u.message.chat.id,keyword):
                            inc.bot.sendMessage(chat_id = u.message.chat.id, text = '관심종목에"' + keyword + '"가 삭제되었습니다.')
                        else:
                            inc.bot.sendMessage(chat_id = u.message.chat.id, text = '관심종목에 없는 종목입니다.')
                    
                    else:
                        inc.bot.sendMessage(chat_id = u.message.chat.id, text = '입력방식이 잘못되었습니다. 추가/삭제를 선택해주시기 바랍니다.')

                # 예외처리
                else :
                    inc.bot.sendMessage(chat_id = u.message.chat.id, text = '입력방식이 잘못되었습니다.')
                    continue
            
            # 종목 일자별 변화율
            elif temp[0] == '!조회':
                keyword = temp[1]

                if len(temp) == 3:
                    try:
                        period = int(temp[2])
                    except:
                        inc.bot.sendMessage(chat_id = u.message.chat.id, text = '기간은 숫자로 입력해주시기 바랍니다.')
                        continue

                # 기본값 지정
                elif len(temp) == 2:
                    period = 7

                # 입력방식이 잘못된경우 리턴
                else:
                    inc.bot.sendMessage(chat_id = u.message.chat.id, text = '입력방식이 잘못되었습니다.')
                    continue

                # 종목코드가 없는 경우
                if stock.getcode(keyword) is None:
                    inc.bot.sendMessage(chat_id = u.message.chat.id, text = '상장되지않은 회사입니다.')
                    continue
                
                inc.bot.sendMessage(chat_id = u.message.chat.id, text = stock.info(keyword,period))

             # 지정가 설정
            elif temp[0] == '!지정가':

                if temp[1] == '조회':

                    # 전체 조회
                    if len(temp) == 2:

                        result = command.readLimit(u.message.chat.id)

                        # 조회결과가 없는 경우
                        if result is None:
                            inc.bot.sendMessage(chat_id = u.message.chat.id, text = '설정된 지정가가 없습니다.')

                        text = ''
                        for k,v in result.items():
                            text = text + k + '의 지정가\n'

                            if 'high' in v:
                                text = text + '⦁ 상향 지정가: ' + str(format(int(v['high']), ',')) + '원\n'

                            if 'low' in v:
                                text = text + '⦁ 하향 지정가: ' + str(format(int(v['low']), ',')) + '원\n'
                            
                        inc.bot.sendMessage(chat_id = u.message.chat.id, text = text)
                        
                    # 종목 지정가 조회
                    elif len(temp) == 3:

                        result = command.readLimit(u.message.chat.id,keyword)
                        
                        # 조회결과가 없는 경우
                        if result is None:
                            inc.bot.sendMessage(chat_id = u.message.chat.id, text = keyword + '의 지정가가 없습니다.')
                            continue
                        
                        text = keyword + '의 지정가\n'

                        if 'high' in result:
                            text = text + '⦁ 상향 지정가: ' + str(format(int(result['high']), ',')) + '원\n'

                        if 'low' in result:
                            text = text + '⦁ 하향 지정가: ' + str(format(int(result['low']), ',')) + '원\n'
                        inc.bot.sendMessage(chat_id = u.message.chat.id, text = text)

                    # 예외처리
                    else :
                        inc.bot.sendMessage(chat_id = u.message.chat.id, text = '입력방식이 잘못되었습니다.')
                        continue
                    
                elif temp[1] == '추가':

                    # 입력방식이 잘못된경우 리턴
                    if len(temp) != 4:
                        inc.bot.sendMessage(chat_id = u.message.chat.id, text = '입력방식이 잘못되었습니다.')
                        continue

                    # 종목코드가 없는 경우
                    if stock.getcode(keyword) is None:
                        inc.bot.sendMessage(chat_id = u.message.chat.id, text = '상장되지않은 회사입니다.')
                        continue

                    # 지정가 숫자가 아닌경우 예외처리
                    try:
                        price = int(temp[3])
                    except:
                        inc.bot.sendMessage(chat_id = u.message.chat.id, text = '지정가는 숫자로 입력해주시기 바랍니다.')
                        continue
                    
                    # 현재가 확인
                    now = stock.now(keyword)

                    if now is None:
                        inc.bot.sendMessage(chat_id = u.message.chat.id, text = '주식api에 문제가 생겼습니다. 관리자에게 문의주시기 바랍니다.')
                        continue

                    # 지정가 판단후 디비 입력
                    if price == now:
                        inc.bot.sendMessage(chat_id = u.message.chat.id, text = '현재가격과 동일해서 등록하지 않습니다.')
                        continue

                    elif price > now:
                        table = 'high'
                    
                    else:
                        table = 'low'
                    result = command.createLimit(u.message.chat.id, keyword, table, price)

                    # 지정가 확인 답장
                    if result:
                        inc.bot.sendMessage(chat_id = u.message.chat.id, text = keyword + '의 지정가: ' 
                        + str(format(price,',')) + '원이 ' + ( '상향' if table == 'high' else '하향' ) + '지정가로 등록되었습니다.')
                    else:
                        inc.bot.sendMessage(chat_id = u.message.chat.id, text = '알 수 없는 이유로 등록되지 않았습니다.')
                
                elif temp[1] == '삭제':
                    
                    # 입력방식이 잘못된경우 리턴
                    if len(temp) != 3:
                        inc.bot.sendMessage(chat_id = u.message.chat.id, text = '입력방식이 잘못되었습니다.')
                        continue

                    if command.deleteLimit(u.message.chat.id, keyword):
                        inc.bot.sendMessage(chat_id = u.message.chat.id, text = '등록된 지정가가 삭제되었습니다.')
                    else:
                        inc.bot.sendMessage(chat_id = u.message.chat.id, text = '남아있는 지정가가 없습니다.')
        
                else :
                    inc.bot.sendMessage(chat_id = u.message.chat.id, text = '해당된 명령어가 없습니다. /help를 입력하여 다시 확인바랍니다.')
    except:
        continue

# 메세지 저장
if updates :
    command.close(updates[-1]['update_id'])
    
inc.close()