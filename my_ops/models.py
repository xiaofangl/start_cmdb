from __future__ import unicode_literals

from django.db import models


# Create your models here.
class OperationLog(models.Model):
    LOG_LEVEL = (
        ('0', 'SUCCESS'),
        ('1', 'WANTING'),
        ('2', 'FAILED')
    )
    action = models.CharField(u'', max_length=45, default='')
    status = models.BooleanField(default=False)
    level = models.CharField(u'', max_length=30, default='0', null=True)
    desc = models.CharField(u'', max_length=256, null=True)

    # user = models
    created = models.DateTimeField(auto_now=True)
    is_del = models.BooleanField(default=False)
