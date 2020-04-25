from django.db import models
from django.urls import reverse

from django_mysql.models import ListCharField

from .lotto import get_lotto_number, get_all_lotto_number_count

COUNT_WORD_DICTIONARY = {
        1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
        6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
        11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen',
        16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen', 20: 'twenty',
        21: 'twenty_one', 22: 'twenty_two', 23: 'twenty_three', 24: 'twenty_four', 25: 'twenty_five',
        26: 'twenty_six', 27: 'twenty_seven', 28: 'twenty_eight', 29: 'twenty_nine', 30: 'thirty',
        31: 'thirty_one', 32: 'thirty_two', 33: 'thirty_three', 34: 'thirty_four', 35: 'thirty_five',
        36: 'thirty_six', 37: 'thirty_seven', 38: 'thirty_eight', 39: 'thirty_nine', 40: 'forty',
        41: 'forty_one', 42: 'forty_two', 43: 'forty_three', 44: 'forty_four', 45: 'forty_five'
    }


class LottoCountManager(models.Manager):

    def update_new_lotto(self, lotto_count_id, drwNo):
        """ 업데이트 할 로또ID와 회차번호를 파라미터로 받아서 업데이트."""
        lotto = get_lotto_number(drwNo).values()

        try:
            transaction = self.model.objects.get(id=lotto_count_id)
        except Exception as e:
            raise ValueError('해당 ID의 LottoCount가 없습니다')

        if drwNo in transaction.drwNos:
            # 입력받은 회차가 이미 기록된 데이터라면 ValueError 발생
            raise ValueError('이미 저장되어 있는 회차입니다.')
        else:
            # 기록된 데이터가 아닐경우 drwNos에 회차 기록
            transaction.drwNos.append(drwNo)

            for _, value in enumerate(lotto):
                word = COUNT_WORD_DICTIONARY[value]

                # 기존에 있던 field값을 가져오고
                field_value = getattr(transaction, word)
                # 그 값에 +1
                field_value += 1
                # 그후 그 값을 필드값으로 저장
                setattr(transaction, word, field_value)

            try:
                transaction.save()
            except Exception as e:
                print('저장 에러', e)
        return transaction

    def create_many_lotto_count(self, final, first=1):
        lotto = get_all_lotto_number_count(final)
        transaction = self.model(final_drwNo=final, first_drwNo=first)

        for index, value in enumerate(lotto):
            if index == 0:
                continue

            word = COUNT_WORD_DICTIONARY[index]
            setattr(transaction, word, value)

        for drwNo in range(first, final+1):
            transaction.drwNos.append(drwNo)

        try:
            transaction.save()
        except Exception as e:
            print('저장 에러', e)

        return transaction


class LottoCount(models.Model):
    first_drwNo = models.PositiveIntegerField(default=0)  # 카운팅하는 로또 데이터의 시작 회수
    final_drwNo = models.PositiveIntegerField(default=0)  # 마지막 회수

    one = models.PositiveIntegerField(default=0)
    two = models.PositiveIntegerField(default=0)
    three = models.PositiveIntegerField(default=0)
    four = models.PositiveIntegerField(default=0)
    five = models.PositiveIntegerField(default=0)
    six = models.PositiveIntegerField(default=0)
    seven = models.PositiveIntegerField(default=0)
    eight = models.PositiveIntegerField(default=0)
    nine = models.PositiveIntegerField(default=0)
    ten = models.PositiveIntegerField(default=0)
    eleven = models.PositiveIntegerField(default=0)
    twelve = models.PositiveIntegerField(default=0)
    thirteen = models.PositiveIntegerField(default=0)
    fourteen = models.PositiveIntegerField(default=0)
    fifteen = models.PositiveIntegerField(default=0)
    sixteen = models.PositiveIntegerField(default=0)
    seventeen = models.PositiveIntegerField(default=0)
    eighteen = models.PositiveIntegerField(default=0)
    nineteen = models.PositiveIntegerField(default=0)
    twenty = models.PositiveIntegerField(default=0)
    twenty_one = models.PositiveIntegerField(default=0)
    twenty_two = models.PositiveIntegerField(default=0)
    twenty_three = models.PositiveIntegerField(default=0)
    twenty_four = models.PositiveIntegerField(default=0)
    twenty_five = models.PositiveIntegerField(default=0)
    twenty_six = models.PositiveIntegerField(default=0)
    twenty_seven = models.PositiveIntegerField(default=0)
    twenty_eight = models.PositiveIntegerField(default=0)
    twenty_nine = models.PositiveIntegerField(default=0)
    thirty = models.PositiveIntegerField(default=0)
    thirty_one = models.PositiveIntegerField(default=0)
    thirty_two = models.PositiveIntegerField(default=0)
    thirty_three = models.PositiveIntegerField(default=0)
    thirty_four = models.PositiveIntegerField(default=0)
    thirty_five = models.PositiveIntegerField(default=0)
    thirty_six = models.PositiveIntegerField(default=0)
    thirty_seven = models.PositiveIntegerField(default=0)
    thirty_eight = models.PositiveIntegerField(default=0)
    thirty_nine = models.PositiveIntegerField(default=0)
    forty = models.PositiveIntegerField(default=0)
    forty_one = models.PositiveIntegerField(default=0)
    forty_two = models.PositiveIntegerField(default=0)
    forty_three = models.PositiveIntegerField(default=0)
    forty_four = models.PositiveIntegerField(default=0)
    forty_five = models.PositiveIntegerField(default=0)

    objects = LottoCountManager()

    drwNos = ListCharField(  # 몇회차의 번호들이 업데이트 되어있는지 확인하는 필드
        base_field=models.IntegerField(),
        size=4,
        max_length=(4 * 2000),
        blank=True
    )

    def __str__(self):
        return str(self.pk) + ' LottoCount' + str(self.first_drwNo) + '-' + str(self.final_drwNo)

    def update_first_and_final(self):
        if len(self.drwNos) == 0:
            raise ValueError('update 할 일자가 없습니다.')
        self.first_drwNo = min(self.drwNos)
        self.final_drwNo = max(self.drwNos)
        self.save()

    def get_absolute_url(self):
        return reverse('analyzer:show_lotto_count', args=[self.pk])
