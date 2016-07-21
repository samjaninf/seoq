from tenant_schemas.test.cases import TenantTestCase
from tenant_schemas.test.client import TenantClient, TenantRequestFactory
from django.core.urlresolvers import reverse
from django.db import connection
from django.conf import settings

from selenium import webdriver

from .models import Client
from hub.users.models import User


class TestViews(TenantTestCase):
    def setUp(self):
        connection.set_schema_to_public()
        self.client = TenantClient(self.tenant)
        self.factory = TenantRequestFactory(self.tenant)
        self.user = User.objects.create(username='user')

    def test_create(self):
        response = self.client.get(reverse('customers:create'))
        self.assertEqual(response.status_code, 302)
