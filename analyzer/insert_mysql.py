import mysql.connector

from config.secrets import get_secret, get_file
from analyzer.lotto import get_all_lotto_number_count
from analyzer.admin import get_new_drwNo


def convert_to_mysql_data(final, first=1):
    """ MySQL에 정의된 스키마대로 데이터를 변환하기 위한 함수,
    Lotto Count 데이터에 drwNo data, boolean data, len data 추가
    tuple 데이터로 반환."""

    lotto_count = get_all_lotto_number_count(final)

    # 카운팅 정렬이기 때문에 첫번째 인덱스를 제거
    lotto_count.pop(0)
    # ID, first_drwNo, final_drwNo
    drwNo_data = [0, first, final]
    # all, a_year, six_months, three_months, a_month
    boolean_data = [0, 0, 0, 0, 0]
    # len(drwNos)
    len_data = ''
    # drwNos data를 '1, 2, 3, 4' 같이 표현하기 위한 로직.
    for drwNo in range(first, final+1):
        if drwNo == final:
            len_data += str(drwNo)
        else:
            len_data += str(drwNo) + ','
    lotto_count.append(len_data)

    mysql_data = drwNo_data + lotto_count + boolean_data

    return tuple(mysql_data)


def insert(data):
    """ MySQL INSERT를 위한 func"""
    secrets_file = get_file()

    # secrets.json 에서 비밀 변수들을 가져옴.
    user = get_secret('MYSQL_USER', secrets_file)
    password = get_secret('MYSQL_PASSWORD', secrets_file)

    # 가져온 비밀변수들로 DB connect.
    cnx = mysql.connector.connect(user=user,
                                  password=password,
                                  host='db',
                                  database='lotto-analyzer-mysql')
    cursor = cnx.cursor()

    add_lotto_count = ("INSERT INTO analyzer_lottocount "
                       "VALUES (%s, %s, %s, "
                       "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
                       "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
                       "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
                       "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
                       "%s, %s, %s, %s, %s,"
                       "%s,"
                       "%s, %s, %s, %s, %s)")

    data_lotto_count = data

    cursor.execute(add_lotto_count, data_lotto_count)
    cnx.commit()

    cursor.close()
    cnx.close()


new_drwNo = get_new_drwNo()
insert(convert_to_mysql_data(new_drwNo))