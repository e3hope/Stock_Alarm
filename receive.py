import telegram
import psycopg2
from . import inc

#bot을 선언
bot = telegram.Bot(token = inc.token)

# 마지막 업데이트목록
lastupdatesql = 'SELECT update_id FROM Lastupdate'
inc.cursor.execute(lastupdatesql)
offset = inc.cursor.fetchone()

#업데이트
updates = bot.getUpdates(offset = offset[0])

# 데이터 입력
for u in updates :
    
    # 남아있는 데이터 넘기기
    if u['update_id'] == offset[0] :
        continue

    # 회원 입력
    if u.message.text == '/start' :
        sql = 'INSERT INTO User (chat_id, id, name, date) VALUES(%s, %s, %s)'
        inc.cursor.execute(sql, (u.message.chat.id, u.message.chat.username, u.message.chat.last_name + u.message.chat.first_name))
        bot.sendMessage(chat_id = u.message.chat.id, text = '/help를 눌러 도움말을 확인하세요.')
        inc.conn.commit()

    # 종목 입력
    elif u.message.text.startswith('@') :
        code = u.message.text.replace('@', '')

        # 있으면 삭제
        try:
            sql = 'DELETE Bookmark WHERE code = %s AND chat_id = %s'
            inc.cursor.execute(sql, (code, u.message.chat.id))
            bot.sendMessage(chat_id = u.message.chat.id, text = '관심종목에"' + code + '"가 삭제되었습니다.')
            inc.conn.commit()

        # 없으면 추가
        except:
            sql = 'INSERT INTO Bookmark (code, chat_id, date) VALUES (%s, %s)'
            inc.cursor.execute(sql, (code, u.message.chat.id))
            bot.sendMessage(chat_id = u.message.chat.id, text = '관심종목에"' + code + '"가 추가되었습니다.')
            inc.conn.commit()

    # 도움말
    # elif u.message.text == '/help' :
    #     bot.sendMessage(chat_id = u.message.chat.id, text='@keyword를 입력해 주세요. ex)@리버풀\n'
    #                     '|입력시 다른기사도 확인 할 수 있습니다. ex)@리버풀|맨유\n'
    #                     '/link입력시 기사의 원문 링크도 확인 할 수 있습니다.')

# 메세지 저장
if updates :
    updatesql = 'UPDATE Lastupdate SET update_id = %s'
    inc.cursor.execute(updatesql, updates[-1]['update_id'])
    inc.conn.commit()
    
inc.conn.close()