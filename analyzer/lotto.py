import time
import requests


def get_lotto_number(drwNo):
    """ 회차에 따른 당첨번호와 보너스 번호 요청"""
    url = 'https://www.nlotto.co.kr/common.do?method=getLottoNumber&drwNo=' + str(drwNo)
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
        raise ValueError('lotto 불러오기 실패')


def get_all_lotto_number_count(final, first=1):
    """ 전체 회차의 번호 빈도수를 요청하기, counting 정렬 활용"""

    # 시작할 회차 번호
    drwNo = first
    # counting 정렬을 위한 list, 첫번째 인덱스는 버리고 사용해야함. 0이라는 로또번호는 없기 때문.
    count_list = [0] * 46

    while True:
        if drwNo > final:
            print(drwNo-1, ' ok')
            return count_list

        if drwNo % 10 == 0:
            print(drwNo, ' ok')

        # Lotto 요청이 짧은 시간에 많을 경우 connection 을 거부해버림. 그렇기에 딜레이가 필요함
        if drwNo % 50 == 0:
            time.sleep(10)

        try:
            lotto = list(get_lotto_number(drwNo).values())
        except Exception as e:
            print(e)
            return count_list
        else:
            for index, value in enumerate(lotto):
                count_list[value] += 1

        drwNo += 1
