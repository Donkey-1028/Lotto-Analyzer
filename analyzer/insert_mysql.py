import mysql.connector
from config.secrets import get_secret, get_file


def insert():
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
    data_lotto_count = (20, 1, 908,
                        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1,
                        1,
                        0, 0, 0, 0, 0)

    cursor.execute(add_lotto_count, data_lotto_count)
    cnx.commit()

    cursor.close()
    cnx.close()


insert()
