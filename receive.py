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
            inc.bot.sendMessage(chat_id = u.message.chat.id, text='!관심종목 {종목} - 관심종목으로 지정됩니다. 관심종목으로 지정시 15:35분에 종가 가격을 알람으로 보냅니다. ex) !삼성전자\n'
                            '!관심종목 {종목} - 재입력 시 관심종목에서 삭제됩니다.\n'
                            '!종목 {기간} - 기간별 변화율을 보여줍니다. ex) !삼성전자 7\n'
                            '!지정가 {종목} {가격} - 지정된 가격이 오면 알림을 보냅니다. ex) !지정가 삼성전자 50000\n'
                            '!지정가 {종목} {가격} - 재입력 시 지정된 가격을 수정해줍니다.\n'
                            '!지정가삭제 {종목} - 입력 시 지정가 알림을 삭제합니다.')

        if u.message.text.startswith('!'):
            
            # 종목코드 추출
            temp = u.message.text.split()
            keyword = temp[1]

            # 관심종목 지정
            if temp[0] == '!관심종목':
                
                if len(temp) != 2:
                    inc.bot.sendMessage(chat_id = u.message.chat.id, text = '입력방식이 잘못되었습니다.')
                    continue

                # 종목코드가 없는 경우
                if stock.getcode(keyword) is None:
                    inc.bot.sendMessage(chat_id = u.message.chat.id, text = '상장되지않은 회사입니다.')
                    continue

                result = command.bookmark(u.message.chat.id,keyword)

                if result == 'insert':
                    inc.bot.sendMessage(chat_id = u.message.chat.id, text = '관심종목에"' + keyword + '"가 추가되었습니다.')
                elif result == 'delete':
                    inc.bot.sendMessage(chat_id = u.message.chat.id, text = '관심종목에"' + keyword + '"가 삭제되었습니다.')
                else:
                    inc.bot.sendMessage(chat_id = u.message.chat.id, text = '알수없는 오류로 인해 작동되지않았습니다. 관리자에게 문의주시기 바랍니다.')
            
            # 종목 일자별 변화율
            elif temp[0] == '!기간조회':
                
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

                # 입력방식이 잘못된경우 리턴
                if len(temp) != 3:
                    inc.bot.sendMessage(chat_id = u.message.chat.id, text = '입력방식이 잘못되었습니다.')
                    continue

                # 종목코드가 없는 경우
                if stock.getcode(keyword) is None:
                    inc.bot.sendMessage(chat_id = u.message.chat.id, text = '상장되지않은 회사입니다.')
                    continue

                price = temp[2]
                now = stock.now(keyword)

                # 지정가 판단후 디비 입력
                if price == now:
                    inc.bot.sendMessage(chat_id = u.message.chat.id, text = '현재가격과 동일해서 등록하지 않습니다.')
                    continue

                elif price > now:
                    table = 'high'
                elif price < now:
                    table = 'low'

                # 지정가 확인 답장
                if command.limit(u.message.chat.id,keyword,table,price):
                    inc.bot.sendMessage(chat_id = u.message.chat.id, text = keyword + '의 지정가' + price + '원이 등록되었습니다.')
                else:
                    inc.bot.sendMessage(chat_id = u.message.chat.id, text = '알 수 없는 이유로 등록되지 않았습니다.')
                
            elif temp[0] == '!지정가삭제':
                
                # 입력방식이 잘못된경우 리턴
                if len(temp) != 2:
                    inc.bot.sendMessage(chat_id = u.message.chat.id, text = '입력방식이 잘못되었습니다.')
                    continue

                if command.limit_delete(u.message.chat.id, keyword):
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