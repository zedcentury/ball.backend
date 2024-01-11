import json
import os.path

from django.core.management import BaseCommand
from django.utils.text import slugify

from common.models import ClassName
from config.settings import BASE_DIR
from user.models import User, Pupil, Parent


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(os.path.join(BASE_DIR, 'common', 'management', 'commands', 'data.json'), 'r') as json_file:
            data = json.load(json_file)
            for d in data:
                pupil_text = d['name']
                class_name_text = d['class']
                parents_text = d['parents']

                class_name, _ = ClassName.objects.get_or_create(name=class_name_text)

                pupil_username = slugify(pupil_text).replace('-', '_')

                if User.objects.filter(username=pupil_username).exists():
                    pupil_username += '2'

                print("Pupil:", pupil_username)
                pupil_user = User.objects.create_user(username=pupil_username, password=pupil_username,
                                                      full_name=pupil_text, user_type=User.UserTypeChoices.PUPIL)
                pupil = Pupil.objects.create(user=pupil_user, class_name=class_name)

                for parent_text in parents_text:
                    parent_username = slugify(parent_text).replace('-', '_')
                    print("Parent:", parent_username)

                    parent_user = User.objects.filter(username=parent_username).first()
                    if parent_user is None:
                        parent_user = User.objects.create_user(username=parent_username, password=parent_username,
                                                               full_name=parent_text,
                                                               user_type=User.UserTypeChoices.PARENT)

                    parent, _ = Parent.objects.get_or_create(user=parent_user)
                    if _:
                        print(_)
                    parent.children.add(pupil)
                    parent.save()
