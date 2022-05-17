import os

from weasyprint import HTML
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
import traceback

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CustomUser, TrinhDoHocVan, PhongHoc, LopHoc, MonHoc, NamHoc, GiaoVien, HocSinh, GiangDay, DiemSo, \
    HanhKiem, HocKy


def student_home(request):
    return render(request, 'student_templates/home_content.html')


def view_classroom(request):
    hoc_sinh = HocSinh.objects.get(mahs=request.user)
    lop = LopHoc.objects.get(ma_lop=hoc_sinh.lop.ma_lop)
    nam_hoc = NamHoc.objects.get(hien_tai=True)
    hoc_ky = HocKy.objects.get(hien_tai=True)
    hanh_kiem = HanhKiem.objects.get(nam_hoc=nam_hoc, hoc_ky=hoc_ky, mahs=hoc_sinh)
    context = {
        "lop": lop,
        "hanh_kiem": hanh_kiem,
        "hoc_sinh": hoc_sinh,
        "nam_hoc": nam_hoc,
        "hoc_ky": hoc_ky,
    }
    return render(request, 'student_templates/view_classroom_template.html', context)


def xem_tkb(request):
    hoc_sinh = HocSinh.objects.get(mahs=request.user)
    lop = LopHoc.objects.get(ma_lop=hoc_sinh.lop.ma_lop)

    context = {
        "link_meet": lop.meetLink,
    }
    return render(request, 'student_templates/view_tuition_student_tempale.html', context)


@csrf_exempt
def student_get_tuition(request):
    if request.accepts("application/json") and request.method == "POST":
        hoc_sinh = HocSinh.objects.get(mahs=request.user)
        lop = LopHoc.objects.get(ma_lop=hoc_sinh.lop.ma_lop)
        nam_hoc = NamHoc.objects.get(hien_tai=True)
        hoc_ky = HocKy.objects.get(hien_tai=True)
        try:
            filter_gd = GiangDay.objects.filter(ma_lop=lop, nam_hoc=nam_hoc, hoc_ky=hoc_ky)
            list_gd = []
            for item in filter_gd:
                small_data = {"id": item.id, "thu": item.thu, "mon": item.magv.day_mon.ten_mon, "1": item.tiet_1,
                              "2": item.tiet_2, "3": item.tiet_3, "4": item.tiet_4, "5": item.tiet_5, "6": item.tiet_6,
                              "7": item.tiet_7, "8": item.tiet_8, "9": item.tiet_9}
                list_gd.append(small_data)
            return JsonResponse(json.dumps(list_gd), content_type="application/json", safe=False)
        except Exception:
            traceback.print_exc()
            return JsonResponse({"error": "try"}, status=400)
    return JsonResponse({"error": "if"}, status=400)


def tkb_hs_pdf(request):
    dirname = os.path.dirname(__file__) + "\\tmp"
    # data
    hoc_sinh = HocSinh.objects.get(mahs=request.user)
    lop = LopHoc.objects.get(ma_lop=hoc_sinh.lop.ma_lop)
    nam_hoc = NamHoc.objects.get(hien_tai=True)
    hoc_ky = HocKy.objects.get(hien_tai=True)
    giang_day = GiangDay.objects.filter(ma_lop=lop, nam_hoc=nam_hoc, hoc_ky=hoc_ky)

    lst_sang = [['Trống' for j in range(6)] for i in range(5)]
    lst_chieu = [['Trống' for j in range(6)] for i in range(4)]

    for gd in giang_day:
        if gd.tiet_1 is True:
            lst_sang[0][gd.thu - 2] = gd.magv.day_mon.ten_mon
        if gd.tiet_2 is True:
            lst_sang[1][gd.thu - 2] = gd.magv.day_mon.ten_mon
        if gd.tiet_3 is True:
            lst_sang[2][gd.thu - 2] = gd.magv.day_mon.ten_mon
        if gd.tiet_4 is True:
            lst_sang[3][gd.thu - 2] = gd.magv.day_mon.ten_mon
        if gd.tiet_5 is True:
            lst_sang[4][gd.thu - 2] = gd.magv.day_mon.ten_mon

        if gd.tiet_6 is True:
            lst_chieu[0][gd.thu - 2] = gd.magv.day_mon.ten_mon
        if gd.tiet_7 is True:
            lst_chieu[1][gd.thu - 2] = gd.magv.day_mon.ten_mon
        if gd.tiet_8 is True:
            lst_chieu[2][gd.thu - 2] = gd.magv.day_mon.ten_mon
        if gd.tiet_9 is True:
            lst_chieu[3][gd.thu - 2] = gd.magv.day_mon.ten_mon

    context = {
        'namhoc': nam_hoc.mo_ta,
        'hocky': hoc_ky.hoc_ky,
        'lop': lop.ten_lop,
        'lst_sang': lst_sang,
        'lst_chieu': lst_chieu,
    }
    html_string = render_to_string('pdf_templates/tkb_hs_template.html', context)

    file_name = nam_hoc.nam_hoc + '-' + hoc_ky.hoc_ky + '-' + lop.ma_lop + '.pdf'

    html = HTML(string=html_string)
    html.write_pdf(target=dirname + '\\' + file_name)

    fs = FileSystemStorage(dirname)
    with fs.open(file_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'
        return response
    return response


def view_personal_mark(request):
    nam_hoc = NamHoc.objects.get(hien_tai=True)
    hoc_ky = HocKy.objects.get(hien_tai=True)
    hoc_sinh = HocSinh.objects.get(mahs=request.user)
    ds_ds = DiemSo.objects.filter(mahs=hoc_sinh, nam_hoc=nam_hoc, hoc_ky=hoc_ky)
    list_ds = []
    for item in ds_ds:
        list_ds.append(item)
    context = {
        'ds_ds': list_ds,
    }
    return render(request, 'student_templates/view_personal_mark_template.html', context)

@csrf_exempt
def bang_diem_hs_pdf(request):
    dirname = os.path.dirname(__file__) + "\\tmp"
    # data
    nam_hoc = NamHoc.objects.get(hien_tai=True)
    hoc_ky = HocKy.objects.get(hien_tai=True)
    hoc_sinh = HocSinh.objects.get(mahs=request.user)
    ds_ds = DiemSo.objects.filter(mahs=hoc_sinh, nam_hoc=nam_hoc, hoc_ky=hoc_ky)
    list_ds = []
    for item in ds_ds:
        list_ds.append(item)

    context = {
        'namhoc': nam_hoc.mo_ta,
        'hocky': hoc_ky.hoc_ky,
        'hoc_sinh': hoc_sinh,
        "bang_diem": list_ds,
    }
    html_string = render_to_string('pdf_templates/bang_diem_hs_template.html', context)

    file_name = 'bang-diem-' + hoc_sinh.mahs.username + '.pdf'

    html = HTML(string=html_string)
    html.write_pdf(target=dirname + '\\' + file_name)

    fs = FileSystemStorage(dirname)
    with fs.open(file_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'
        return response
    return response


def profile_student(request):
    return render(request, 'student_templates/profile_student_template.html')


@csrf_exempt
def luu_doi_mat_khau_hoc_sinh(request):
    if request.accepts("application/json") and request.method == "POST":
        old_password = request.POST.get('old_password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if request.user.check_password(old_password):
                username = request.user.username
                request.user.set_password(password1)
                request.user.save()
                user = authenticate(username=username, password=password1)
                login(request, user)
                return JsonResponse({"success": "Đổi mật khẩu thành công"}, content_type="application/json", safe=False)
            else:
                return JsonResponse({"error": "Lỗi: mật khẩu cũ không dúng"}, status=400)
        else:
            return JsonResponse({"error": "Lỗi: mật  khẩu mới không trùng nhau"}, status=400)
