# Stock_Alarm

## 시작 방법
telegram에서 BotFather를 추가하여 botFather에서 bot을 생성한다.
생성된 봇과 같이 알려주는 token을 inc.py에 추가하여 저장한다.
주식정보는 finance-datareader api 활용

## 파일 설명
### setting file
- inc.py

### class/method file
- stock.py      # 주식 api method file
- command.py    # 명령문 db연결 관련 method file

### cron file 
- receive.py    # telegram 메세지 실행 file
- limit.py      # 지정가 전송 file
- close.py      # 종가 전송 file
- stockcode_update.py   # 주식종목코드 갱신 file

## 구현 기능 및 실행 명령어
/start - 시작 / 회원정보 자동 추가

/help - 기능 및 명령어 설명

!조회 {종목} {기간} - 기간별 변화율을 보여줍니다. ex) !조회 삼성전자 7

!관심종목 조회 - 나의 관심종목 리스트를 조회합니다. ex) !관심종목 조회

!관심종목 추가 {종목} - 관심종목으로 지정됩니다. ex) !관심종목 추가 삼성전자

!관심종목 삭제 {종목} - 관심종목에서 삭제됩니다. ex) !관심종목 삭제 삼성전자

!지정가 조회 - 설정된 지정가를 보여줍니다. ex) !지정가 조회 삼성전자

!지정가 조회 {종목} - 개별종목의 설정된 지정가를 보여줍니다. ex) !지정가 조회 삼성전자

!지정가 추가 {종목} {가격} - 지정된 가격이 오면 알림을 보냅니다. ex) !지정가 추가 삼성전자 50000

!지정가 추가 {종목} {가격} - 재입력 시 지정된 가격을 수정해줍니다. ex) !지정가 추가 삼성전자 60000

!지정가 삭제 {종목} - 입력 시 지정가 알림을 삭제합니다. ex) !지정가 삭제 삼성전자
