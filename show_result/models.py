from django.db import models

# Create your models here.


class house(models.Model):
    position = models.CharField('地址', max_length=256)
    lat = models.FloatField('緯度', blank=True, null=True)
    lon = models.FloatField('經度', blank=True, null=True)
    unitPrice = models.FloatField('每平方公尺單價', blank=True)
    update_time = models.DateTimeField('更新時間', auto_now=True)

    def __str__(self):
        return '地址: %s 每平方公尺售價: %s' % (self.position, self.unitPrice)
