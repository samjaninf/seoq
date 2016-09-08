import json
import requests
import os
from django.core.files import File

import tempfile

from django.core.management.base import BaseCommand
from balystic.client import Client
from seoq.users.models import User


class Command(BaseCommand):
    help = 'Moves the data from generics field to local user model'

    def handle(self, *args, **kwargs):
        user_list = Client().get_users({'isPro': '1'})
        user_list_fixed = user_list['users']
        user_list_fixed.append(user_list['owner'])
        users = User.objects.all()
        for user in user_list_fixed:
            temp = users.filter(username=user['username'])
            if not isinstance(user['generics'], dict):
                generics = json.loads(user['generics'])
            else:
                generics = user['generics']
            if len(temp) == 0:
                User.objects.create(username=user['username'],
                                    email=user['email'],
                                    generics=generics)
            else:
                db_user = temp[0]
                db_user.generics = generics
                db_user.save()
        users = User.objects.all()
        for user in users:
            if isinstance(user.generics, unicode):
                user.generics = json.loads(user.generics)
                user.save()
            temp = user.generics
            try:
                user.website_url = temp['website_url']
                user.areas_of_expertise = temp['areas_of_expertise']
                user.areas_of_expertise_other = temp['areas_of_expertise_other']
                user.languages = temp['languages']
                user.languages_other = temp['languages_other']
                user.google_account = temp['google_url']
                user.location = temp['location']
                user.phone_number = temp['phone']
                user.company_name = temp['company_name']
                image = temp['company_logo']
                if image:
                    image = 'https://omega.seoq.com/media/' + image
                    # http://stackoverflow.com/questions/16174022/download-a-remote-image-and-save-it-to-a-django-model
                    result = requests.get(
                        image, stream=True)

                    lf = tempfile.NamedTemporaryFile()
                    file_name = image.split('/')[-1]

                    for block in result.iter_content(1024 * 8):

                        # If no more file then stop
                        if not block:
                            break
                        lf.write(block)

                    user.company_logo.save(
                        file_name,
                        File(lf))
                else:
                    user.company_logo = ''
                user.save()
            except KeyError:
                continue
