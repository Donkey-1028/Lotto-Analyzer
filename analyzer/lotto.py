import requests


def get_lotto_number(drwNo):
    """ 회차에 따른 당첨번호와 보너스 번호 요청"""
    url = 'http://www.nlotto.co.kr/common.do?method=getLottoNumber&drwNo=' + str(drwNo)
    req = requests.get(url)
    res = req.json()

    if res['returnValue'] == 'success':
        context = {
            'first': res['drwtNo1'],
            'second': res['drwtNo2'],
            'third': res['drwtNo3'],
            'forth': res['drwtNo4'],
            'fifth': res['drwtNo5'],
            'sixth': res['drwtNo6'],
            'bonus': res['bnusNo']
        }

        return context
    else:
        return ValueError('lotto 불러오기 실패')


def get_all_lotto_number_count(final, first=1):
    """ 전체 회차의 번호 빈도수를 요청하기, counting 정렬 활용"""
    drwNo = first  # 시작할 회차 번호
    count_list = [0] * 46

    while True:
        if drwNo > final:
            print()
            return count_list

        if drwNo % 10 == 0:
            print('.', end='')

        lotto = list(get_lotto_number(drwNo).values())
        for index, value in enumerate(lotto):
            count_list[value] += 1

        drwNo += 1

print(get_all_lotto_number_count(10))