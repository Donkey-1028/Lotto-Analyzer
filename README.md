    개발환경 잡기
    1.docker-compose build > 이미지 생성
    2.docker-compose up > 컴포즈파일 실행
    3.mysql에 접속하여 root 정보 변경,
    4.settings.py database 설정에 맞게 유저 생성.
    5.생성된 유저에 권한 주기.
    
    shell 이용해서 LOTTO 데이터 추가하기.
    1.python manage.py shell
    2.import mysql.connector
    3.from analyzer.lotto import get_all_lotto_number_count
    3.exec(open('analyzer/insert_mysql.py').read())