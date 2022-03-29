from django.db import models
# Create your models here.


class TinTuc(models.Model):
    tieu_de = models.CharField(max_length=255, default='')
    ngay_tao = models.DateTimeField(auto_now_add=True)
    tao_boi = models.ForeignKey('qldh.AdminUser', on_delete=models.CASCADE)
    noi_dung = models.TextField(max_length=1000)
