import requests

from django.test import TestCase

from .models import LottoCount
from .lotto import get_lotto_number, get_all_lotto_number_count


class LottoAPITest(TestCase):
    """ lotto.py Test"""

    def setUp(self):
        self.test_url = 'http://www.nlotto.co.kr/common.do?method=getLottoNumber&drwNo='

    def test_get_lotto_number_with_wrong_drwNo(self):
        """ 잘못된 회차의 로또 데이터를 요청하였을 때"""
        with self.assertRaisesMessage(ValueError, 'lotto 불러오기 실패'):
            get_lotto_number(-1)

        with self.assertRaisesMessage(ValueError, 'lotto 불러오기 실패'):
            get_lotto_number(10000)

    def test_get_lotto_number_compare_requests_number(self):
        """ requests 모듈을 이용하여 불러온 로또 데이터와
        가공하기 위해 만든 function의 데이터를 비교 """
        req = requests.get(self.test_url + '1')
        request_response = req.json()
        function_response = get_lotto_number(1)
        for i in range(1, 7, 1):
            self.assertIn(request_response['drwtNo'+str(i)], function_response.values())

    def test_get_all_lotto_number_count(self):
        """ 지정한 회차까지 총 당첨번호의 갯수를 이용하여 제대로 요청이 되었는지 테스트 """
        try_count = 5  # 몇회차 까지의 번호를 가져오는지 설정
        all_count = 0  # 해당한 회차까지 총 번호의 갯수, ex) 5회의 회차라면 35개의 당첨 번호가 있어야함
        result = get_all_lotto_number_count(try_count)

        for _, value in enumerate(result):
            all_count += value

        self.assertEqual(try_count * 7, all_count)


class LottoCountTest(TestCase):
    """ LottoCountTest Model, Manager Test"""

    def setUp(self):
        self.model = LottoCount.objects.create()

    def test_update_new_lotto(self):
        """ update_new_lotto 메소드 테스트"""
        LottoCount.objects.update_new_lotto(self.model.id, 1)

        # 제대로 update가 되었다면 ten 필드 값은 1이 됨
        first_value = LottoCount.objects.get(id=self.model.id).ten

        # 마찬가지로 1회차에는 번호 1이 없었기 때문에 필드값은 0이여야 함
        second_value = LottoCount.objects.get(id=self.model.id).one

        self.assertEqual(first_value, 1)
        self.assertNotEqual(second_value, 1)
