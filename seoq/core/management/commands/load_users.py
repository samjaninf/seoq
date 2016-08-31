from django.core.management.base import BaseCommand
from seoq.users.models import User
from balystic.client import Client
import json

class Command(BaseCommand):
    help = 'Moves the data from generics field to local user model'

    def handle(self, *args, **kwargs):
        user_list = Client().get_users({'isPro': '1'})
        user_list_fixed = user_list['users']
        user_list_fixed.append(user_list['owner'])
        users = User.objects.all()
        for user in user_list_fixed:
            temp = users.filter(username=user['username'])
            generics = json.loads(user['generics'])
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
                user.save()
            except KeyError:
                continue
