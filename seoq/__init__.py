# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .asynchronous.celery import app as celery_app
__version__ = '0.1.0'
__version_info__ = tuple([int(num) if num.isdigit() else num for num in __version__.replace('-', '.', 1).split('.')])