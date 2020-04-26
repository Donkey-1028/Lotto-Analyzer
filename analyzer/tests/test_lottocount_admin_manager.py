from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.urls import reverse

from analyzer.models import LottoCount
from analyzer.admin import LottoCountAdminManager


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

    def test_update_new_lotto_action(self):
        """ update_new_lotto action 테스트"""
        url = reverse('admin:analyzer_lottocount_changelist')
        model = LottoCount.objects.create_many_lotto_count(1)
        self.client.login(username='test_admin', password='testadminpassword')
        data = {
            'action': 'update_new_lotto_action',
            '_selected_action': model.id
        }
        self.client.post(url, data)
        model = LottoCount.objects.get(id=model.id)

        self.assertEqual(len(model.drwNos), 2)