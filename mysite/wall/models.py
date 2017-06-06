# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Post(models.Model):
    post_text = models.TextField()
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.post_text
