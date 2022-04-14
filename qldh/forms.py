from django import forms
import datetime
from .models import TrinhDoHocVan, MonHoc, PhongHoc, NamHoc, GiaoVien, LopHoc
from crispy_bootstrap5.bootstrap5 import *
from crispy_forms.bootstrap import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *


gender_list = (
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ')
    )

grade_list = (
        ('Khối 10', 'Khối 10'),
        ('Khối 11', 'Khối 11'),
        ('Khối 12', 'Khối 12')
    )

# Học vấn
try:
    trinh_do = TrinhDoHocVan.objects.all()
    ds_trinh_do = []
    for td in trinh_do:
        tdhv = (td.trinh_do, td.mo_ta_trinh_do)
        ds_trinh_do.append(tdhv)
except:
    ds_trinh_do = []

# Môn học
try:
    mon_hoc = MonHoc.objects.all()
    ds_mon = []
    for m in mon_hoc:
        mon = (m.ma_mon, m.ten_mon)
        ds_mon.append(mon)
except:
    ds_mon = []

# Giáo viên chủ nhiệm
try:
    giao_vien = GiaoVien.objects.all()
    ds_giao_vien = []
    for gv in giao_vien:
        gvcn = (gv.magv, gv.magv.get_full_name())
        ds_giao_vien.append(gvcn)
except:
    ds_giao_vien = []

# Phòng học
try:
    phong = PhongHoc.objects.all()
    ds_phong = []
    for p in phong:
        ph = (p.ma_phong, p.ten_phong)
        ds_phong.append(ph)
except:
    ds_phong = []

# Lớp học
try:
    lop_hoc = LopHoc.objects.all()
    ds_lop = []
    for l in lop_hoc:
        lop = (l.ma_lop, l.ten_lop)
        ds_lop.append(lop)
except:
    ds_lop = []


class AddTeacherForm(forms.Form):
    last_name = forms.CharField(label="Nhập họ",
                                max_length=50,
                                required=True,
                                widget=forms.TextInput)
    first_name = forms.CharField(label="Nhập tên",
                                 max_length=50,
                                 required=True,
                                 widget=forms.TextInput)
    que_quan = forms.CharField(label="Nhập quê quán",
                               max_length=255,
                               required=True,
                               widget=forms.TextInput)
    so_dien_thoai = forms.CharField(label="Số điện thoại",
                                    max_length=10,
                                    required=True,
                                    widget=forms.TextInput)

    gioi_tinh = forms.ChoiceField(label="Giới tính",
                                  choices=gender_list,
                                  widget=forms.Select)
    ngay_sinh = forms.DateField(label="Ngày sinh",
                                widget=forms.TextInput(
                                    attrs={'type': 'date'}
                                ))
    trinh_do = forms.ChoiceField(label="Trình độ học vấn",
                                choices=ds_trinh_do,
                                widget=forms.Select)
    day_mon = forms.ChoiceField(label="Môn giảng dạy",
                                choices=ds_mon,
                                widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Div(FloatingField('last_name'), css_class='col-md'),
                Div(FloatingField('first_name'), css_class='col-md')),
            Row(Div(FloatingField('gioi_tinh'), css_class='col-md'),
                Div(FloatingField('so_dien_thoai'), css_class='col-md')),
            Div(FloatingField('que_quan')),
            Row(Div(FloatingField('ngay_sinh'), css_class='col-md')),
            Row(Div(FloatingField('trinh_do'), css_class='col-md'),
                Div(FloatingField('day_mon'), css_class='col-md')),
        )


class EditTeacherForm(forms.Form):
    username = forms.CharField(label="Mã giáo viên",
                               max_length=50,
                               widget=forms.TextInput(attrs={"readonly": ""}))
    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"readonly": ""}))
    last_name = forms.CharField(label="Nhập họ",
                                max_length=50,
                                required=True,
                                widget=forms.TextInput)
    first_name = forms.CharField(label="Nhập tên",
                                 max_length=50,
                                 required=True,
                                 widget=forms.TextInput)
    que_quan = forms.CharField(label="Nhập quê quán",
                               max_length=255,
                               required=True,
                               widget=forms.TextInput)
    so_dien_thoai = forms.CharField(label="Số điện thoại",
                                    max_length=10,
                                    required=True,
                                    widget=forms.TextInput)
    gioi_tinh = forms.ChoiceField(label="Giới tính",
                                  choices=gender_list,
                                  widget=forms.Select)
    ngay_sinh = forms.DateField(label="Ngày sinh",
                                widget=forms.TextInput(
                                    attrs={'type': 'date'}
                                ))
    trinh_do = forms.ChoiceField(label="Trình độ học vấn",
                                 choices=ds_trinh_do,
                                 widget=forms.Select)
    day_mon = forms.ChoiceField(label="Môn giảng dạy",
                                choices=ds_mon,
                                widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Div(FloatingField('username'), css_class='col-md'),
                Div(FloatingField('email'), css_class='col-md')),
            Row(Div(FloatingField('last_name'), css_class='col-md'),
                Div(FloatingField('first_name'), css_class='col-md')),
            Row(Div(FloatingField('gioi_tinh'), css_class='col-md'),
                Div(FloatingField('so_dien_thoai'), css_class='col-md')),
            Div(FloatingField('que_quan')),
            Row(Div(FloatingField('ngay_sinh'), css_class='col-md')),
            Row(Div(FloatingField('trinh_do'), css_class='col-md'),
                Div(FloatingField('day_mon'), css_class='col-md')),
        )


class AddClassroomForm(forms.Form):
    ten_lop = forms.CharField(label="Nhập tên lớp",
                              max_length=50,
                              required=True,
                              widget=forms.TextInput)
    khoi = forms.ChoiceField(label="Khối",
                             required=True,
                             choices=grade_list,
                             widget=forms.Select)
    phong = forms.ChoiceField(label="Phòng học",
                              choices=ds_phong,
                              required=True,
                              widget=forms.Select)
    giao_vien_chu_nhiem = forms.ChoiceField(label="Giáo viên chủ nhiệm",
                                            choices=ds_giao_vien,
                                            required=True,
                                            widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Div(FloatingField('ten_lop'), css_class='col-md'),
                Div(FloatingField('khoi'), css_class='col-md')),
            Row(Div(FloatingField('phong'), css_class='col-md'),
                Div(FloatingField('giao_vien_chu_nhiem'), css_class='col-md')),
        )


class EditClassroomForm(forms.Form):
    ma_lop = forms.CharField(label="Mã lớp",
                             widget=forms.TextInput)
    ten_lop = forms.CharField(label="Nhập tên lớp",
                              max_length=50,
                              required=True,
                              widget=forms.TextInput)
    khoi = forms.ChoiceField(label="Khối",
                             required=True,
                             choices=grade_list,
                             widget=forms.Select)
    phong = forms.ChoiceField(label="Phòng học",
                              choices=ds_phong,
                              required=True,
                              widget=forms.Select)
    giao_vien_chu_nhiem = forms.ChoiceField(label="Giáo viên chủ nhiệm",
                                            choices=ds_giao_vien,
                                            required=True,
                                            widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Div(FloatingField('ma_lop'), css_class='col-md'),
                Div(FloatingField('ten_lop'), css_class='col-md')),
                Div(FloatingField('khoi'), css_class='col-md'),
            Row(Div(FloatingField('phong'), css_class='col-md'),
                Div(FloatingField('giao_vien_chu_nhiem'), css_class='col-md')),
        )


class AddStudentForm(forms.Form):
    last_name = forms.CharField(label="Nhập họ",
                                max_length=50,
                                required=True,
                                widget=forms.TextInput)
    first_name = forms.CharField(label="Nhập tên",
                                 max_length=50,
                                 required=True,
                                 widget=forms.TextInput)
    que_quan = forms.CharField(label="Nhập quê quán",
                               max_length=255,
                               required=True,
                               widget=forms.TextInput)
    gioi_tinh = forms.ChoiceField(label="Giới tính",
                                  choices=gender_list,
                                  required=True,
                                  widget=forms.Select)
    ngay_sinh = forms.DateField(label="Ngày sinh",
                                widget=forms.TextInput(
                                    attrs={'type': 'date'}
                                ))
    dan_toc = forms.CharField(label="Dân tộc",
                              max_length=255,
                              required=True,
                              widget=forms.TextInput)
    lop = forms.ChoiceField(label="Lớp",
                            choices=ds_lop,
                            required=True,
                            widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Div(FloatingField('last_name'), css_class='col-md'),
                Div(FloatingField('first_name'), css_class='col-md')),
            Row(Div(FloatingField('gioi_tinh'), css_class='col-md'),
                Div(FloatingField('dan_toc'), css_class='col-md')),
            Div(FloatingField('que_quan')),
            Row(Div(FloatingField('ngay_sinh'), css_class='col-md'),
                Div(FloatingField('lop'), css_class='col-md')),
        )


class EditStudentForm(forms.Form):
    username = forms.CharField(label="Mã học sinh",
                               max_length=50,
                               widget=forms.TextInput(attrs={"readonly": ""}))
    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"readonly": ""}))
    last_name = forms.CharField(label="Nhập họ",
                                max_length=50,
                                required=True,
                                widget=forms.TextInput)
    first_name = forms.CharField(label="Nhập tên",
                                 max_length=50,
                                 required=True,
                                 widget=forms.TextInput)
    que_quan = forms.CharField(label="Nhập quê quán",
                               max_length=255,
                               required=True,
                               widget=forms.TextInput)
    gioi_tinh = forms.ChoiceField(label="Giới tính",
                                  choices=gender_list,
                                  widget=forms.Select)
    ngay_sinh = forms.DateField(label="Ngày sinh",
                                widget=forms.TextInput(
                                    attrs={'type': 'date'}
                                ))
    dan_toc = forms.CharField(label="Dân tộc",
                              max_length=255,
                              required=True,
                              widget=forms.TextInput)
    lop = forms.ChoiceField(label="Lớp",
                            choices=ds_lop,
                            required=True,
                            widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Div(FloatingField('username'), css_class='col-md'),
                Div(FloatingField('email'), css_class='col-md')),
            Row(Div(FloatingField('last_name'), css_class='col-md'),
                Div(FloatingField('first_name'), css_class='col-md')),
            Row(Div(FloatingField('gioi_tinh'), css_class='col-md'),
                Div(FloatingField('dan_toc'), css_class='col-md')),
            Div(FloatingField('que_quan')),
            Row(Div(FloatingField('ngay_sinh'), css_class='col-md'),
                Div(FloatingField('lop'), css_class='col-md')),
        )
