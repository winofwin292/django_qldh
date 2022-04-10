from django.contrib import admin

# Register your models here.


from .models import CustomUser, TrinhDoHocVan, PhongHoc, LopHoc, MonHoc, NamHoc, HocKy, GiaoVien, HocSinh, GiangDay, DiemSo, KetQuaHocTap

admin.site.register(MonHoc)
admin.site.register(NamHoc)
admin.site.register(HocKy)
admin.site.register(TrinhDoHocVan)
admin.site.register(CustomUser)
