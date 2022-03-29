# Generated by Django 4.0.1 on 2022-03-20 06:04

from django.db import migrations
from django.db.models.signals import post_migrate
from qldh.models import HocKy, MonHoc, NamHoc


def them_hoc_ky(apps, **kwargs):
    HocKy.objects.get_or_create(hoc_ky='1')
    HocKy.objects.get_or_create(hoc_ky='2')


def them_mon_hoc(apps, **kwargs):
    MonHoc.objects.get_or_create(ma_mon='CN', ten_mon='Công nghệ', tiet_tuan=1)
    MonHoc.objects.get_or_create(ma_mon='DL', ten_mon='Địa lí', tiet_tuan=2)
    MonHoc.objects.get_or_create(ma_mon='GDCD', ten_mon='Giáo dục công dân', tiet_tuan=1)
    MonHoc.objects.get_or_create(ma_mon='HH', ten_mon='Hóa học', tiet_tuan=2)
    MonHoc.objects.get_or_create(ma_mon='LS', ten_mon='Lịch sử', tiet_tuan=1)
    MonHoc.objects.get_or_create(ma_mon='NN', ten_mon='Ngoại ngữ', tiet_tuan=3)
    MonHoc.objects.get_or_create(ma_mon='NV', ten_mon='Ngữ văn', tiet_tuan=4)
    MonHoc.objects.get_or_create(ma_mon='SH', ten_mon='Sinh học', tiet_tuan=2)
    MonHoc.objects.get_or_create(ma_mon='TD', ten_mon='Thể dục', tiet_tuan=2)
    MonHoc.objects.get_or_create(ma_mon='TH', ten_mon='Tin học', tiet_tuan=2)
    MonHoc.objects.get_or_create(ma_mon='T', ten_mon='Toán', tiet_tuan=5)
    MonHoc.objects.get_or_create(ma_mon='VL', ten_mon='Vật lí', tiet_tuan=3)
    MonHoc.objects.get_or_create(ma_mon='QP', ten_mon='Giáo dục quốc phòng', tiet_tuan=1)


def them_nam_hoc(apps, **kwargs):
    for year in range(10, 50):
        nh = str(year) + '-' + str(year + 1)
        mt = '20' + str(year) + ' - ' + '20' + str(year + 1)
        NamHoc.objects.get_or_create(nam_hoc=nh, mo_ta=mt)


class Migration(migrations.Migration):

    dependencies = [
        ('qldh', '0022_alter_lophoc_ma_lop_alter_phonghoc_ma_phong'),
    ]

    operations = [
    ]


post_migrate.connect(them_hoc_ky)
post_migrate.connect(them_nam_hoc)
post_migrate.connect(them_mon_hoc)
