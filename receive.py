import telegram
import psycopg2
import inc

#bot을 선언
bot = telegram.Bot(token = inc.set['Telegram']['token'])

# 마지막 업데이트목록
lastupdatesql = 'SELECT update_id, message_id FROM lastupdate'
inc.cursor.execute(lastupdatesql)
offset = inc.cursor.fetchall()

#업데이트
updates = bot.getUpdates()

# 데이터 입력
for u in updates :

    # 남아있는 데이터 넘기기
    if not offset or u['update_id'] == offset[0] and u['message_id'] == offset[0] :
        continue

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
        code = u.message.text.replace('@', '')

        # 있으면 삭제
        try:
            sql = 'DELETE bookmark WHERE code = %s AND chat_id = %s'
            inc.cursor.execute(sql, (code, u.message.chat.id))
            bot.sendMessage(chat_id = u.message.chat.id, text = '관심종목에"' + code + '"가 삭제되었습니다.')
            inc.conn.commit()

        # 없으면 추가
        except:
            inc.conn.rollback()
            sql = 'INSERT INTO bookmark (code, chat_id, date) VALUES (%s, %s)'
            inc.cursor.execute(sql, (code, u.message.chat.id))
            bot.sendMessage(chat_id = u.message.chat.id, text = '관심종목에"' + code + '"가 추가되었습니다.')
            inc.conn.commit()

    # 도움말
    elif u.message.text == '/help' :
        bot.sendMessage(chat_id = u.message.chat.id, text='@종목을 입력해주세요\n'
                        '기간은 일주일 입니다. (추후 업데이트 예정!)')

# 메세지 저장
if updates :
    updatesql = 'UPDATE lastupdate SET update_id = %s, message_id = %s'
    inc.cursor.execute(updatesql, (updates[-1]['update_id'], updates[-1]['message_id']))
    inc.conn.commit()
    
inc.conn.close()