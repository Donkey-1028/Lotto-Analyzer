import requests


def get_lotto_number(drwNo):
    url = 'http://www.nlotto.co.kr/common.do?method=getLottoNumber&drwNo=' + str(drwNo)
    req = requests.get(url)
    res = req.json()

    if res['returnValue'] == 'success':
        context = {
            'no': res['drwNo'],
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


