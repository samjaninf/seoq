from django.core.management.base import BaseCommand
from seoq.users.models import User
import json


class Command(BaseCommand):
    help = 'Moves the data from generics field to local user model'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            temp = user.generics
            try:
                user.website_url = temp['website_url']
                user.website_url1 = temp['website_url1']
                user.website_url2 = temp['website_url2']
                user.website_url3 = temp['website_url3']
                user.website_url4 = temp['website_url4']
                user.areas_of_expertise = temp['areas_of_expertise']
                user.areas_of_expertise_other = temp['areas_of_expertise_other']
                user.languages = temp['languages']
                user.languages_other = temp['languages_other']
                user.save()
            except KeyError:
                continue
