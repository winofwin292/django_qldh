import traceback
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CustomUser, TrinhDoHocVan, PhongHoc, LopHoc, MonHoc, NamHoc, GiaoVien, HocSinh, GiangDay, DiemSo, \
    HanhKiem, HocKy
import os
from weasyprint import HTML
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string


def teacher_home(request):
    count_tuition = GiangDay.objects.filter(magv=request.user.username).count()
    giang_day = GiangDay.objects.filter(magv=request.user.username)
    try:
        tshs = 0
        for gd in giang_day:
            tshs += gd.ma_lop.si_so
        tshscn = LopHoc.objects.get(giao_vien_chu_nhiem=request.user.username).si_so
    except:
        tshs = 0
        tshscn = 0
    context = {
        "tsgd": count_tuition,
        "tshs": tshs,
        "tshscn": tshscn,
    }
    return render(request, 'teacher_templates/home_content.html', context)


def view_tuition(request):
    return render(request, 'teacher_templates/view_tuition_tempale.html')


@csrf_exempt
def teacher_get_tuition(request):
    if request.accepts("application/json") and request.method == "POST":
        nam_hoc = NamHoc.objects.get(hien_tai=True)
        hoc_ky = HocKy.objects.get(hien_tai=True)
        try:
            filter_gd = GiangDay.objects.filter(magv=request.user.username, nam_hoc=nam_hoc, hoc_ky=hoc_ky)
            list_gd = []
            for item in filter_gd:
                small_data = {"id": item.id, "thu": item.thu, "ma_lop": item.ma_lop.ten_lop, "1": item.tiet_1,
                              "2": item.tiet_2, "3": item.tiet_3, "4": item.tiet_4, "5": item.tiet_5, "6": item.tiet_6,
                              "7": item.tiet_7, "8": item.tiet_8, "9": item.tiet_9}
                list_gd.append(small_data)
            return JsonResponse(json.dumps(list_gd), content_type="application/json", safe=False)
        except Exception:
            traceback.print_exc()
            return JsonResponse({"error": "try"}, status=400)
    return JsonResponse({"error": "if"}, status=400)


def tkb_gv_pdf(request):
    dirname = os.path.dirname(__file__) + "\\tmp"
    # data
    nam_hoc = NamHoc.objects.get(hien_tai=True)
    hoc_ky = HocKy.objects.get(hien_tai=True)
    giao_vien = GiaoVien.objects.get(magv=request.user.username)
    giang_day = GiangDay.objects.filter(magv=giao_vien, nam_hoc=nam_hoc, hoc_ky=hoc_ky)
    lst_sang = [['Trống' for j in range(6)] for i in range(5)]
    lst_chieu = [['Trống' for j in range(6)] for i in range(4)]

    for gd in giang_day:
        if gd.tiet_1 is True:
            lst_sang[0][gd.thu - 2] = gd.ma_lop.ten_lop
        if gd.tiet_2 is True:
            lst_sang[1][gd.thu - 2] = gd.ma_lop.ten_lop
        if gd.tiet_3 is True:
            lst_sang[2][gd.thu - 2] = gd.ma_lop.ten_lop
        if gd.tiet_4 is True:
            lst_sang[3][gd.thu - 2] = gd.ma_lop.ten_lop
        if gd.tiet_5 is True:
            lst_sang[4][gd.thu - 2] = gd.ma_lop.ten_lop

        if gd.tiet_6 is True:
            lst_chieu[0][gd.thu - 2] = gd.ma_lop.ten_lop
        if gd.tiet_7 is True:
            lst_chieu[1][gd.thu - 2] = gd.ma_lop.ten_lop
        if gd.tiet_8 is True:
            lst_chieu[2][gd.thu - 2] = gd.ma_lop.ten_lop
        if gd.tiet_9 is True:
            lst_chieu[3][gd.thu - 2] = gd.ma_lop.ten_lop

    context = {
        'namhoc': nam_hoc.mo_ta,
        'hocky': hoc_ky.hoc_ky,
        'giaovien': giao_vien.magv.last_name + ' ' + giao_vien.magv.first_name,
        'lst_sang': lst_sang,
        'lst_chieu': lst_chieu,
    }
    html_string = render_to_string('pdf_templates/tkb_gv_template.html', context)

    file_name = nam_hoc.nam_hoc + '-' + hoc_ky.hoc_ky + '-' + giao_vien.magv.username + '.pdf'

    html = HTML(string=html_string)
    html.write_pdf(target=dirname + '\\' + file_name)

    fs = FileSystemStorage(dirname)
    with fs.open(file_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'
        return response
    return response


def view_student(request):
    try:
        lop_cn = LopHoc.objects.get(giao_vien_chu_nhiem=request.user.username)
        ds_hs = lop_cn.hocsinh_set.all()
    except:
        ds_hs = []
        messages.error(request, "Giáo viên này không chủ nhiệm lớp nào cả")
    context = {
        "dshs": ds_hs,
        "lop_cn": lop_cn,
    }
    return render(request, 'teacher_templates/view_student_template.html', context)


def dshs_cn_pdf(request):
    dirname = os.path.dirname(__file__) + "\\tmp"
    # data
    nam_hoc = NamHoc.objects.get(hien_tai=True)
    hoc_ky = HocKy.objects.get(hien_tai=True)
    giao_vien = GiaoVien.objects.get(magv=request.user.username)
    try:
        lop_cn = LopHoc.objects.get(giao_vien_chu_nhiem=request.user.username)
        ds_hs = lop_cn.hocsinh_set.all()
    except:
        ds_hs = []

    context = {
        'namhoc': nam_hoc.mo_ta,
        'hocky': hoc_ky.hoc_ky,
        'giaovien': giao_vien.magv.last_name + ' ' + giao_vien.magv.first_name,
        "dshs": ds_hs,
        "lop_cn": lop_cn,
    }
    html_string = render_to_string('pdf_templates/ds_lop_chu_nhiem_template.html', context)

    file_name = 'ds-' + lop_cn.ten_lop + '.pdf'

    html = HTML(string=html_string)
    html.write_pdf(target=dirname + '\\' + file_name)

    fs = FileSystemStorage(dirname)
    with fs.open(file_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'
        return response
    return response


def manage_mark(request):
    nam_hoc = NamHoc.objects.get(hien_tai=True)
    hoc_ky = HocKy.objects.get(hien_tai=True)
    giang_day = GiangDay.objects.filter(magv=request.user.username, nam_hoc=nam_hoc, hoc_ky=hoc_ky)
    list_tmp = []
    list_lh = []

    for item in giang_day:
        if item.ma_lop.ma_lop not in list_tmp:
            list_tmp.append(item.ma_lop.ma_lop)
            lop_hoc = LopHoc.objects.get(ma_lop=item.ma_lop.ma_lop)
            list_lh.append(lop_hoc)
    context = {
        "list_lh": list_lh,
    }
    return render(request, 'teacher_templates/manage_mark_template.html', context)


@csrf_exempt
def lay_danh_sach_hoc_sinh(request):
    if request.accepts("application/json") and request.method == "POST":
        try:
            ma_lop = request.POST.get('ma_lop')
            lop = LopHoc.objects.get(ma_lop=ma_lop)
            giao_vien = GiaoVien.objects.get(magv=request.user.username)
            mon = MonHoc.objects.get(ma_mon=giao_vien.day_mon.ma_mon)
            nam_hoc = NamHoc.objects.get(hien_tai=True)
            hoc_ky = HocKy.objects.get(hien_tai=True)

            filter_hs = HocSinh.objects.filter(lop=lop)

            list_ds = []
            for item in filter_hs:
                ds = DiemSo.objects.get_or_create(mahs=item, nam_hoc=nam_hoc, hoc_ky=hoc_ky, mon=mon)[0]
                small_data = {"id": ds.id, "mhs": item.mahs.username, "hoten": item.mahs.last_name + ' ' + item.mahs.first_name,
                              "m1": ds.m1, "m2": ds.m2, "m3": ds.m3, "p1": ds.p1, "p2": ds.p2, "p3": ds.p3, "p4": ds.p4,
                              "t1": ds.t1, "t2": ds.t2, "t3": ds.t3, "t4": ds.t4, "t5": ds.t5, "t6": ds.t6, "t7": ds.t7,
                              "t8": ds.t8, "hk": ds.hk, "tb": ds.tb}
                list_ds.append(small_data)
            return JsonResponse(json.dumps(list_ds), content_type="application/json", safe=False)
        except Exception:
            traceback.print_exc()
            return JsonResponse({"error": "Lỗi: Tải dữ liệu không thành công"}, status=400)
    return JsonResponse({"error": "Lỗi: Sai phương thức"}, status=400)


@csrf_exempt
def luu_diem_so(request):
    if request.accepts("application/json") and request.method == "POST":
        try:
            id_ds = request.POST.get('id_ds')
            m1 = request.POST.get('m1')
            m2 = request.POST.get('m2')
            m3 = request.POST.get('m3')
            p1 = request.POST.get('p1')
            p2 = request.POST.get('p2')
            p3 = request.POST.get('p3')
            p4 = request.POST.get('p4')
            t1 = request.POST.get('t1')
            t2 = request.POST.get('t2')
            t3 = request.POST.get('t3')
            t4 = request.POST.get('t4')
            t5 = request.POST.get('t5')
            t6 = request.POST.get('t6')
            t7 = request.POST.get('t7')
            t8 = request.POST.get('t8')
            hk = request.POST.get('hk')
            diem_so = DiemSo.objects.get(id=id_ds)
            diem_so.m1 = m1
            diem_so.m2 = m2
            diem_so.m3 = m3
            diem_so.p1 = p1
            diem_so.p2 = p2
            diem_so.p3 = p3
            diem_so.p4 = p4
            diem_so.t1 = t1
            diem_so.t2 = t2
            diem_so.t3 = t3
            diem_so.t4 = t4
            diem_so.t5 = t5
            diem_so.t6 = t6
            diem_so.t7 = t7
            diem_so.t8 = t8
            diem_so.hk = hk
            diem_so.save()
            return JsonResponse({"success": "success"}, content_type="application/json", safe=False)
        except Exception:
            traceback.print_exc()
            return JsonResponse({"error": "Lỗi: Tải dữ liệu không thành công"}, status=400)
    return JsonResponse({"error": "Lỗi: Sai phương thức"}, status=400)


@csrf_exempt
def bang_diem_pdf(request, ma_lop):
    dirname = os.path.dirname(__file__) + "\\tmp"
    # data
    nam_hoc = NamHoc.objects.get(hien_tai=True)
    hoc_ky = HocKy.objects.get(hien_tai=True)
    #ma_lop = request.POST.get('ma_lop')
    lop = LopHoc.objects.get(ma_lop=ma_lop)
    giao_vien = GiaoVien.objects.get(magv=request.user.username)
    mon = MonHoc.objects.get(ma_mon=giao_vien.day_mon.ma_mon)
    filter_bang_diem = DiemSo.objects.filter(nam_hoc=nam_hoc, hoc_ky=hoc_ky, mon=mon)
    list_bang_diem = []
    for item in filter_bang_diem:
        list_bang_diem.append(item)

    context = {
        'namhoc': nam_hoc.mo_ta,
        'hocky': hoc_ky.hoc_ky,
        'giaovien': giao_vien.magv.last_name + ' ' + giao_vien.magv.first_name,
        "bang_diem": list_bang_diem,
        "lop": lop,
        "mon": mon
    }
    html_string = render_to_string('pdf_templates/bang_diem_template.html', context)

    file_name = 'bang-diem-' + lop.ten_lop + '-' + mon.ma_mon + '.pdf'

    html = HTML(string=html_string)
    html.write_pdf(target=dirname + '\\' + file_name)

    fs = FileSystemStorage(dirname)
    with fs.open(file_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'
        return response
    return response


def danh_gia_hanh_kiem(request):
    try:
        lop_cn = LopHoc.objects.get(giao_vien_chu_nhiem=request.user.username)
        ds_hs = HocSinh.objects.filter(lop=lop_cn.ma_lop)
        nam_hoc = NamHoc.objects.get(hien_tai=True)
        hoc_ky = HocKy.objects.get(hien_tai=True)

        list_kq = []
        for item in ds_hs:
            hanh_kiem = HanhKiem.objects.get_or_create(mahs=item, nam_hoc=nam_hoc, hoc_ky=hoc_ky)[0]
            list_kq.append(hanh_kiem)
    except:
        list_kq = []
        messages.error(request, "Giáo viên này không chủ nhiệm lớp nào cả")
    context = {
        "lop_cn": lop_cn,
        "kqht": list_kq,
    }
    return render(request, 'teacher_templates/assessment_student_template.html', context)


# def edit_assessment_student(request, student_id):
#     # lop_cn = LopHoc.objects.get(giao_vien_chu_nhiem=request.user.username)
#     hs = HocSinh.objects.get(mahs=student_id)
#     nam = NamHoc.objects.get(nam_hoc=hs.lop.nam_hoc.nam_hoc)
#     ds = DiemSo.objects.filter(mahs=hs, nam_hoc=nam)
#     kqht = KetQuaHocTap.objects.get(mahs=hs, nam_hoc=nam)
#     list_dg = ("Xuất sắc", "Giỏi", "Khá", "Trung Bình", "Yếu", "Kém")
#     tong_diem = 0.0
#     for d in ds:
#         tong_diem += d.diem
#     diem_tb = round(tong_diem / (ds.count()), 2)
#     # print(diem_tb)
#     context = {
#         "hs": hs,
#         "ds": ds,
#         "kqht": kqht,
#         "list_dg": list_dg,
#         "diem_tb": diem_tb,
#     }
#     return render(request, 'teacher_templates/edit_assessment_student_template.html', context)
#
#
# def edit_assessment_student_save(request, student_id, kqht_id):
#     if request.method != "POST":
#         messages.error(request, "Invalid Method")
#         return redirect('assessment_student')
#     else:
#         xep_loai = request.POST.get('xep_loai')
#         hanh_kiem = request.POST.get('hanh_kiem')
#         try:
#             kqht = KetQuaHocTap.objects.get(id=kqht_id)
#             kqht.xep_loai = xep_loai
#             kqht.hanh_kiem = hanh_kiem
#             kqht.save()
#             messages.success(request, "Đánh giá thành công")
#             return redirect('assessment_student')
#         except:
#             messages.success(request, "Lỗi đánh giá")
#             return redirect('/qldh/chinh_sua_danh_gia_hoc_sinh/' + student_id)


def profile_teacher(request):
    lop_cn = LopHoc.objects.get(giao_vien_chu_nhiem=request.user.username)
    context = {
        "lop_cn": lop_cn,
    }
    return render(request, 'teacher_templates/profile_teacher_template.html', context)


def change_password(request):
    return render(request, 'teacher_templates/change_password_template.html')


def change_password_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('change_password')
    else:
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
                messages.success(request, "Đổi mật khẩu thành công")
                return redirect('change_password')
                # print(request.user.check_password(old_password))
            else:
                # print(request.user.check_password(old_password))
                messages.error(request, "Mật khẩu cũ không đúng")
                return redirect('change_password')
        else:
            messages.error(request, "Mật khẩu mới không trùng nhau")
            return redirect('change_password')
