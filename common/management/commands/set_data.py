import datetime
import random

from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand

from common.models import ClassName
from score.models import Reason, Score, ScoreDaily, ScoreStat
from user.models import User, Teacher, Parent, Pupil

boys = ['Qodir', 'Tohir', 'Anvar', 'Jamol', 'Usmon', 'Po\'lat', 'Yo\'ldosh', 'Kamoliddin', 'Asliddin', 'Doston',
        'Maxmud', 'Erkin', 'Otabek', 'Bekzod', 'Abdulla', 'Ilyos', 'Muhriddin']
girls = ['Malika', 'Jamila', 'Durdona', 'Komila', 'Feruza', 'Mohira', 'Zebo', 'Anora', 'Munisa', 'Odina',
         'Kamola', 'Yulduz', 'Dinora']
hamma_ismlar = boys + girls
undoshlar = 'bcdfghjklmnpqrstvwxyz'
unlilar = 'aeiou'


def get_full_name():
    familiya = random.choice(boys)
    if familiya[-1] in undoshlar:
        familiya += 'ov'
    else:
        familiya += 'yev'
    ism = random.choice(hamma_ismlar)
    if ism in girls:
        familiya += 'a'
    return f'{familiya} {ism}'


class Command(BaseCommand):
    def handle(self, *args, **options):
        Score.objects.all().delete()
        ScoreDaily.objects.all().delete()
        ScoreStat.objects.all().delete()
        Teacher.objects.all().delete()
        Parent.objects.all().delete()
        Pupil.objects.all().delete()
        ClassName.objects.all().delete()
        Reason.objects.all().delete()
        User.objects.all().delete()

        today_datetime = datetime.datetime.now()

        # Classes
        classes = []
        for i in range(1, 12):
            for j in random.choice(['A', 'AB', 'ABV']):
                classes.append(ClassName(name=f'{i}-{j}'))
        ClassName.objects.bulk_create(classes)

        # Admin
        admin_user = User.objects.create_superuser(username='admin',
                                                   password='1',
                                                   full_name=get_full_name())
        admin_user.date_joined = today_datetime - datetime.timedelta(days=random.randint(5, 10))
        admin_user.save()

        # Teacher
        for i in range(1, 21):
            teacher_user = User.objects.create_user(username=f'teacher{i}',
                                                    password='1',
                                                    full_name=get_full_name(),
                                                    user_type=User.UserTypeChoices.TEACHER)
            teacher_user.date_joined = today_datetime - datetime.timedelta(days=random.randint(5, 10))
            teacher_user.save()
            Teacher.objects.create(user=teacher_user)

        # Parent
        for i in range(1, 51):
            parent_user = User.objects.create_user(username=f'parent{i}',
                                                   full_name=get_full_name(),
                                                   password='1',
                                                   user_type=User.UserTypeChoices.PARENT)
            parent_user.date_joined = today_datetime - datetime.timedelta(days=random.randint(5, 10))
            parent_user.save()
            parent = Parent.objects.create(user=parent_user)

            # Pupil
            for j in range(1, random.choice([2, 4])):
                pupil_user = User.objects.create_user(username=f'pupil{i}{j}',
                                                      full_name=get_full_name(),
                                                      password='1',
                                                      user_type=User.UserTypeChoices.PUPIL)
                pupil_user.date_joined = today_datetime - datetime.timedelta(days=random.randint(5, 10))
                pupil_user.save()
                class_name = ClassName.objects.exclude(pupil_to_class_name__user=pupil_user).order_by('?').first()
                pupil_obj = Pupil.objects.create(user=pupil_user, class_name=class_name)
                parent.children.add(pupil_obj)
            parent.save()

        # Reason
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
                'ball': -36
            },
            {
                'text': 'Kitob o\'qib tugatdi',
                'ball': 20
            },
            {
                'text': 'Darsda aktiv qatnashdi',
                'ball': 14
            },
            {
                'text': 'Yomon xulq',
                'ball': -24
            },
        ]
        for reason in reasons:
            Reason.objects.create(text=reason['text'], ball=reason['ball'])

        # Score
        pupils = Pupil.objects.all()
        reasons_length = len(reasons)
        for pupil in pupils:
            current_datetime = pupil.user.date_joined
            days = (today_datetime - current_datetime).days
            for _ in range(days + 1):
                random_reasons = random.sample(reasons, random.randint(1, reasons_length - 1))
                for reason in random_reasons:
                    score = Score.objects.create(pupil=pupil,
                                                 reason=reason['text'],
                                                 ball=reason['ball'])
                    score.created_at = current_datetime
                    score.save()
                    score_daily = ScoreDaily.objects.filter(pupil=pupil, created_at=current_datetime.date()).first()
                    if score_daily is not None:
                        score_daily.ball += reason['ball']
                        score_daily.save()
                    else:
                        score_daily = ScoreDaily.objects.create(pupil=pupil,
                                                                ball=reason['ball'])
                        score_daily.created_at = current_datetime.date()
                        score_daily.save()
                current_datetime += datetime.timedelta(days=1)
