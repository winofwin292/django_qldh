from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.


class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "Giáo Viên"), (3, "Học Sinh"))
    user_type = models.IntegerField(default=1, choices=user_type_data)

    def get_full_name(self):
        return self.last_name + " " + self.first_name


class AdminUser(models.Model):
    ma_admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, to_field='username', primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class TrinhDoHocVan(models.Model):
    trinh_do = models.CharField(max_length=40, primary_key=True)
    mo_ta_trinh_do = models.CharField(default='', max_length=250, unique=True)
    objects = models.Manager()


class PhongHoc(models.Model):
    ma_phong = models.CharField(max_length=8, default='', primary_key=True)
    ten_phong = models.CharField(max_length=50, default='', unique=True)
    so_luong_cho_ngoi = models.IntegerField(default=0)
    objects = models.Manager()

    def get_id(self):
        return self.ma_phong


class MonHoc(models.Model):
    ma_mon = models.CharField(primary_key=True, max_length=5, null=False)
    ten_mon = models.CharField(max_length=50, default='', unique=True, null=False)
    tiet_tuan = models.IntegerField(default=0, null=False)
    objects = models.Manager()


class NamHoc(models.Model):
    nam_hoc = models.CharField(max_length=50, primary_key=True)
    mo_ta = models.CharField(default='', max_length=255, unique=True)
    hien_tai = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return self.nam_hoc + '(' + self.mo_ta + ')'


class HocKy(models.Model):
    hoc_ky = models.CharField(max_length=1, primary_key=True)
    hien_tai = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return "Học Kỳ " + self.hoc_ky


class GiaoVien(models.Model):
    magv = models.OneToOneField(CustomUser, on_delete=models.CASCADE, to_field='username', primary_key=True)
    so_dien_thoai = models.CharField(max_length=10, default='', null=True)
    trinh_do = models.ForeignKey(TrinhDoHocVan, on_delete=models.CASCADE)
    que_quan = models.TextField(default='')
    ngay_sinh = models.DateField(default=datetime(1900, 1, 1))
    gioi_tinh = models.CharField(max_length=50, default='')
    day_mon = models.ForeignKey(MonHoc, on_delete=models.CASCADE)
    profile_pic = models.FileField(default='')
    objects = models.Manager()

    def get_id(self):
        return self.magv


class LopHoc(models.Model):
    ma_lop = models.CharField(primary_key=True, max_length=8, default='')
    ten_lop = models.CharField(max_length=50, default='', unique=True)
    phong = models.OneToOneField(PhongHoc, on_delete=models.CASCADE)
    si_so = models.IntegerField(default=0)
    giao_vien_chu_nhiem = models.OneToOneField(GiaoVien, on_delete=models.CASCADE)
    khoi = models.CharField(max_length=50)
    nam_hoc = models.ForeignKey(NamHoc, on_delete=models.CASCADE, null=True)
    objects = models.Manager()

    def get_id(self):
        return self.ma_lop


class HocSinh(models.Model):
    mahs = models.OneToOneField(CustomUser, on_delete=models.CASCADE, to_field='username', primary_key=True)
    lop = models.ForeignKey(LopHoc, on_delete=models.DO_NOTHING)
    que_quan = models.TextField()
    ngay_sinh = models.DateField(default=datetime(1900, 1, 1))
    gioi_tinh = models.CharField(max_length=50)
    dan_toc = models.CharField(max_length=50)
    profile_pic = models.FileField(default="")
    objects = models.Manager()

    def get_id(self):
        return self.mahs


class GiangDay(models.Model):
    magv = models.ForeignKey(GiaoVien, on_delete=models.CASCADE)
    thu = models.IntegerField(null=False, default=8,
                              validators=[MaxValueValidator(7),
                                          MinValueValidator(2)]
                              )
    ma_lop = models.ForeignKey(LopHoc, on_delete=models.CASCADE)

    nam_hoc = models.ForeignKey(NamHoc, on_delete=models.CASCADE)
    hoc_ky = models.ForeignKey(HocKy, on_delete=models.CASCADE, default="0")

    tiet_1 = models.BooleanField(default=False, blank=True)
    tiet_2 = models.BooleanField(default=False, blank=True)
    tiet_3 = models.BooleanField(default=False, blank=True)
    tiet_4 = models.BooleanField(default=False, blank=True)
    tiet_5 = models.BooleanField(default=False, blank=True)
    tiet_6 = models.BooleanField(default=False, blank=True)
    tiet_7 = models.BooleanField(default=False, blank=True)
    tiet_8 = models.BooleanField(default=False, blank=True)
    tiet_9 = models.BooleanField(default=False, blank=True)
    objects = models.Manager()

    class Meta:
        unique_together = (('ma_lop', 'nam_hoc', 'hoc_ky', 'thu', 'tiet_1', 'tiet_2', 'tiet_3', 'tiet_4', 'tiet_5'
                            , 'tiet_6', 'tiet_7', 'tiet_8', 'tiet_9'),)


class KetQuaHocTap(models.Model):
    mahs = models.ForeignKey(HocSinh, on_delete=models.CASCADE)
    xep_loai = models.CharField(max_length=50, default="Chưa đánh giá")
    hanh_kiem = models.CharField(max_length=50, default="Chưa đánh giá")
    nam_hoc = models.ForeignKey(NamHoc, on_delete=models.CASCADE)
    hoc_ky = models.ForeignKey(HocKy, on_delete=models.CASCADE, default="0")
    objects = models.Manager()


class DiemSo(models.Model):
    mahs = models.ForeignKey(HocSinh, on_delete=models.CASCADE)
    nam_hoc = models.ForeignKey(NamHoc, on_delete=models.CASCADE)
    hoc_ky = models.ForeignKey(HocKy, on_delete=models.CASCADE, default="0")
    mon = models.ForeignKey(MonHoc, on_delete=models.CASCADE)
    diem = models.FloatField(default=0.0, null=True)
    trang_thai = models.CharField(max_length=50, default="Chưa nhập")
    objects = models.Manager()


class DiemSo_ChiTiet(models.Model):
    mads = models.OneToOneField(DiemSo, on_delete=models.CASCADE, primary_key=True)
    diem_mieng = models.FloatField(default=0.0)
    diem_15_phut = models.FloatField(default=0.0)
    diem_45_phut = models.FloatField(default=0.0)
    diem_thi = models.FloatField(default=0.0)
    objects = models.Manager()


# Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminUser.objects.create(ma_admin=instance)
        if instance.user_type == 2:
            GiaoVien.objects.create(magv=instance, trinh_do=TrinhDoHocVan.objects.get(trinh_do="TC"),
                                    day_mon=MonHoc.objects.get(ma_mon="GDCD"))
        if instance.user_type == 3:
            HocSinh.objects.create(mahs=instance, lop=LopHoc.objects.get(ma_lop="LH000001"))


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminuser.save()
    if instance.user_type == 2:
        instance.giaovien.save()
    if instance.user_type == 3:
        instance.hocsinh.save()
