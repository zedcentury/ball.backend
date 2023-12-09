import random

from django.core.management import BaseCommand

from common.models import ClassName
from score.models import Reason
from user.models import User, Teacher, Parent, Pupil


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(1, 12):
            for j in random.choice(['A', 'AB', 'ABV']):
                ClassName.objects.create(name=f'{i}-{j}')

        User.objects.create_superuser(username='admin', password='1')

        for i in range(1, 13):
            teacher = User.objects.create_user(username=f'teacher{i}', full_name='A B', password='1',
                                               user_type=User.UserTypeChoices.TEACHER)
            Teacher.objects.create(user=teacher)

        for i in range(1, 151):
            parent = User.objects.create_user(username=f'parent{i}', full_name='A B', password='1',
                                              user_type=User.UserTypeChoices.PARENT)
            parent_obj = Parent.objects.create(user=parent)
            for j in range(1, random.choice([2, 3])):
                pupil = User.objects.create_user(username=f'pupil{i}{j}', full_name='A B', password='1',
                                                 user_type=User.UserTypeChoices.PUPIL)
                class_name = ClassName.objects.exclude(pupil_to_class_name__user=pupil).order_by('?').first()
                pupil_obj = Pupil.objects.create(user=pupil, class_name=class_name)
                parent_obj.children.add(pupil_obj)
                parent_obj.save()

        reasons = [
            {
                'text': 'Darsga kelmadi',
                'ball': -20
            },
            {
                'text': 'Uyga vazifani bajardi',
                'ball': 12
            },
            {
                'text': 'Darsdan qochdi',
                'ball': -40
            },
            {
                'text': 'Kitob o\'qib tugatdi',
                'ball': 36
            },
            {
                'text': 'Darsda aktiv qatnashdi',
                'ball': 14
            }
        ]
        for reason in reasons:
            Reason.objects.create(text=reason['text'], ball=reason['ball'])

