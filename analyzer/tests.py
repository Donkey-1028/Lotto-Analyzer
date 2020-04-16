import requests

from django.test import TestCase

from .models import LottoCount, COUNT_WORD_DICTIONARY
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
        self.first_lotto_count = [10, 23, 29, 33, 37, 40, 16]  # 1회 당첨 번호

    def test_update_new_lotto_with_wrong_id(self):
        """ 존재하지 않는 LottoCount를 이용해서 update_new_lotto를 하려고 할 때 실패 테스트"""
        with self.assertRaisesMessage(ValueError, '해당 ID의 LottoCount가 없습니다'):
            LottoCount.objects.update_new_lotto(3, 1)

    def test_update_duplicate_lotto(self):
        """ 이미 저장된 데이터를 저장하려고 할 때 실패테스트"""
        model = LottoCount.objects.create(drwNos=1)
        with self.assertRaisesMessage(ValueError, '이미 저장되어 있는 회차입니다.'):
            LottoCount.objects.update_new_lotto(model.id, 1)

    def test_update_new_lotto(self):
        """ update_new_lotto 메소드 테스트"""
        api_lotto_list = get_lotto_number(1)
        LottoCount.objects.update_new_lotto(self.model.id, 1)
        model = LottoCount.objects.get(id=self.model.id)

        for _, value in enumerate(api_lotto_list.values()):
            """api로 받아온 dictionary 형태의 lotto 데이터중 value 값들을 이용하여
            field의 값을 가져옴. 필드의 값이 1일경우 테스트 통과"""
            word = COUNT_WORD_DICTIONARY[value]
            field_value = getattr(model, word)
            self.assertEqual(field_value, 1)

    def test_update_new_lotto_drwNos(self):
        """ update_new_lotto 메소드를 진행후 drwNos가 제대로 저장되는지"""
        LottoCount.objects.update_new_lotto(self.model.id, 2)
        model = LottoCount.objects.get(id=self.model.id)

        self.assertIn(2, model.drwNos)

    def test_create_many_lotto_count(self):
        """ create_many_lotto_count 테스트 """

        # API를 이용해서 얻어온 로또 count list
        api_lotto_list = get_all_lotto_number_count(10)
        # create_many_lotto_count로 생성한 다수의 로또 count
        LottoCount.objects.create_many_lotto_count(10)
        model = LottoCount.objects.get(id=2)

        for index, value in enumerate(api_lotto_list):
            """ API를 이용해서 얻어온 데이터와, create_many_lotto_count를 이용해서 생성한
            데이터가 일치하는지 테스트"""
            if index == 0:
                continue

            word = COUNT_WORD_DICTIONARY[index]
            field_value = getattr(model, word)
            #  얻어온 데이터와 저장된 데이터가 같은지
            self.assertEqual(field_value, value)