import requests

from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.models import User
from django.urls import reverse

from .models import LottoCount, COUNT_WORD_DICTIONARY
from .lotto import get_lotto_number, get_all_lotto_number_count
from .admin import LottoCountAdminManager


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

    def test_update_first_and_final(self):
        """ LottoCount set_first_and_final 메소드 테스트"""
        model = LottoCount.objects.create_many_lotto_count(1)
        LottoCount.objects.update_new_lotto(model.id, 2)
        model = LottoCount.objects.get(id=model.id)

        # 해당 메소드를 실행할 경우 first_drwNo에는 drwNos중 최솟값, final_drwNo에는 최대값으로 설정
        model.update_first_and_final()

        self.assertTrue(model.first_drwNo, 1)
        self.assertTrue(model.final_drwNo, 2)

    def test_wrong_update_first_and_final(self):
        model = LottoCount.objects.create()
        with self.assertRaisesMessage(ValueError, 'update 할 일자가 없습니다.'):
            model.update_first_and_final()


class MockRequest:
    """ Request를 위한 HttpRequest 모조 클래스"""
    def __init__(self, user=None, first_drwNo=None, final_drwNo=None, lotto_id=None, drwNo=None):
        self.user = user
        #  request.GET.get('key') 를 흉내내기 위한 클래스 속성
        self.GET = {
            'first_drwNo': first_drwNo,
            'final_drwNo': final_drwNo,
            'lotto_id': lotto_id,
            'drwNo': drwNo
        }


class LottoCountAdminManagerTest(TestCase):
    """ LottoCountAdminManager 테스트"""
    def setUp(self):
        self.super_user = User.objects.create_superuser(username='test_admin', password='testadminpassword')
        self.user = User.objects.create_user(username='test_user', password='testpassword')
        self.model_admin = LottoCountAdminManager(model=LottoCount, admin_site=AdminSite())

    def test_create_index_like_doc(self):
        """ 공식문서처럼 URL 을 이용한 테스트가 아닌 AdminManager를 통해서 테스트.
        관리자 계정으로 request할 경우 create_index 뷰가 정상적인 상태코드 반환"""
        request = MockRequest(user=self.super_user)
        response = self.model_admin.create_index(request=request)

        self.assertEqual(response.status_code, 200)

    def test_create_index(self):
        """ 일반적인 URL을 이용한 AdminManager 테스트."""
        url = reverse('admin:create_index')
        self.client.login(username='test_admin', password='testadminpassword')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_index_without_staff_permission_like_doc(self):
        """ staff 가 아닌 유저가 create_index 뷰에 접근하려고 할 때 테스트.
        예상된 response_code는 권한 없음이지만 아예 response_code가 반환하기 전에 에러가 발생한다.
        예상되는 이유로는 데코레이터에 의해 staff 권한이 없을 경우 자동으로 admin:login으로 redirect 되는데
        이때 HttpRequest의 build_absolute_uri 메소드를 이용해서 해당 URL이 지정된다. 하지만 앞서 정의한
        모조품 Request인 MockReuqest 클래스는 해당 메소드가 없기 때문에 build_absolute_uri 메소드가 없다고
        AttributeError 가 발생한다. """
        request = MockRequest(user=self.user)
        with self.assertRaisesMessage(AttributeError, ''):
            self.model_admin.create_index(request=request)

    def test_create_index_without_staff_permission(self):
        """ 위의 테스트와 마찬가지로 권한 없다는 status code인 401으로 예상을 했지만
        staff_member_required 데코레이터에 의해 redirect 되기 때문에 302 코드 반환."""
        url = reverse('admin:create_index')
        self.client.login(username='test_user', password='testpassword')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_create_lotto_like_doc(self):
        """ create_lotto 메소드 테스트, document에 있는 방식대로 테스트"""
        request = MockRequest(user=self.super_user, first_drwNo=1, final_drwNo=1)

        response = self.model_admin.create_lotto(request=request)
        model = LottoCount.objects.first()
        self.assertIsNotNone(model)
        self.assertEqual(response.status_code, 302)

    def test_create_lotto(self):
        """ 기존의 URL 을 이용한 create_lotto 메소드 테스트"""
        url = reverse('admin:create_lotto')
        data = {
            'first_drwNo': 1,
            'final_drwNo': 1,
        }
        self.client.login(username='test_admin', password='testadminpassword')
        response = self.client.get(url, data=data)
        model = LottoCount.objects.first()

        self.assertIsNotNone(model)
        self.assertEqual(response.status_code, 302)

    def test_update_index_like_doc(self):
        """ update_index 테스트"""
        request = MockRequest(user=self.super_user)
        response = self.model_admin.update_index(request=request)

        self.assertEqual(response.status_code, 200)

    def test_update_index(self):
        """ update_index 테스트"""
        url = reverse('admin:update_index')
        self.client.login(username='test_admin', password='testadminpassword')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_update_lotto_like_doc(self):
        """ update_lotto 메서드 document 방식대로 테스트"""
        model = LottoCount.objects.create_many_lotto_count(1)
        request = MockRequest(user=self.super_user, lotto_id=model.id, drwNo=2)
        self.model_admin.update_lotto(request=request)
        model = LottoCount.objects.get(id=model.id)

        self.assertEqual(model.first_drwNo, 1)
        self.assertEqual(model.final_drwNo, 2)

    def test_update_lotto(self):
        """ 기존의 URL 을 이용한 update_lotto 메서드 테스트"""
        url = reverse('admin:update_lotto')
        model = LottoCount.objects.create_many_lotto_count(1)
        data = {
            'lotto_id': model.id,
            'drwNo': 2
        }
        self.client.login(username='test_admin', password='testadminpassword')
        self.client.get(url, data=data)
        model = LottoCount.objects.get(id=model.id)
        model.update_first_and_final()

        self.assertEqual(model.first_drwNo, 1)
        self.assertEqual(model.final_drwNo, 2)