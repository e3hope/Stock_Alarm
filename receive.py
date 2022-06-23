import telegram
import psycopg2
import inc
import stock

#bot을 선언
bot = telegram.Bot(token = inc.set['Telegram']['token'])

# 마지막 업데이트목록
lastupdatesql = 'SELECT update_id FROM lastupdate'
inc.cursor.execute(lastupdatesql)
offset = inc.cursor.fetchone()

#업데이트
updates = bot.getUpdates(offset = offset[0])

# 데이터 입력
for u in updates :
    
    # 남아있는 데이터 넘기기
    if u['update_id'] == offset[0] :
        continue

    try:

        # 회원 입력
        if u.message.text == '/start' :
        
            try:
                sql = 'INSERT INTO member (chat_id, id, name) VALUES (%s, %s, %s)'
                inc.cursor.execute(sql, (u.message.chat.id, u.message.chat.username, u.message.chat.last_name + u.message.chat.first_name))
                inc.conn.commit()
                bot.sendMessage(chat_id = u.message.chat.id, text = '/help를 눌러 도움말을 확인하세요.')
            except:
                inc.conn.rollback()
                bot.sendMessage(chat_id = u.message.chat.id, text = '이미 등록된 정보입니다.')
        
        # 종목 입력
        elif u.message.text.startswith('@') :
            
            # 종목코드 추출
            keyword = u.message.text.replace('@', '')
            
            # 종목코드가 없는 경우
            if stock.stock_code(keyword) is None:
                bot.sendMessage(chat_id = u.message.chat.id, text = '상장되지않은 회사입니다.')
                continue

            # 관심종목 여부 확인
            try:
                bookmarksql = 'SELECT name FROM bookmark WHERE name = %s AND chat_id = %s'
                inc.cursor.execute(bookmarksql, (keyword, str(u.message.chat.id)))
                result = inc.cursor.fetchone()

                # 없으면 추가
                if result is None:
                    sql = 'INSERT INTO bookmark (name, chat_id) VALUES (%s, %s)'
                    inc.cursor.execute(sql, (keyword, str(u.message.chat.id)))
                    inc.conn.commit()
                    bot.sendMessage(chat_id = u.message.chat.id, text = '관심종목에"' + keyword + '"가 추가되었습니다.')

                # 있으면 삭제
                else:
                    sql = 'DELETE FROM bookmark WHERE name = %s AND chat_id = %s'
                    inc.cursor.execute(sql, (keyword, str(u.message.chat.id)))
                    inc.conn.commit()
                    bot.sendMessage(chat_id = u.message.chat.id, text = '관심종목에"' + keyword + '"가 삭제되었습니다.')

            except:
                    inc.conn.rollback()

        # 종목 일자별 변화율
        elif u.message.text.startswith('!') :
            
            # 종목 및 기간 추출
            temp = u.message.text.split()

            # 입력방식이 잘못된경우 리턴
            if len(temp) > 2:
                bot.sendMessage(chat_id = u.message.chat.id, text = '입력방식이 잘못되었습니다.')
                continue

            keyword = temp[0].replace('!', '')
            period = int(temp[1]) if len(temp) == 2 else 7

            # 종목코드가 없는 경우
            if stock.stock_code(keyword) is None:
                bot.sendMessage(chat_id = u.message.chat.id, text = '상장되지않은 회사입니다.')
                continue

            bot.sendMessage(chat_id = u.message.chat.id, text = stock.stock_info(keyword,period))

        # 도움말
        elif u.message.text == '/help' :
            bot.sendMessage(chat_id = u.message.chat.id, text='@종목을 입력하면 관심종목 지정!ex) @삼성전자\n'
                            '!종목 기간 을입력시 기간별 변화율을 보여줍니다. ex) !삼성전자 7')
    except:
        continue

# 메세지 저장
if updates :
    updatesql = 'UPDATE lastupdate SET update_id = %s'
    inc.cursor.execute(updatesql, [updates[-1]['update_id']])
    inc.conn.commit()
    
inc.conn.close()