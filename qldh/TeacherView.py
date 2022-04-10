import traceback
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CustomUser, TrinhDoHocVan, PhongHoc, LopHoc, MonHoc, NamHoc, GiaoVien, HocSinh, GiangDay, DiemSo, KetQuaHocTap, HocKy
from .forms import MarkForm
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

    file_name =nam_hoc.nam_hoc + '-' + hoc_ky.hoc_ky + '-' + giao_vien.magv.username + '.pdf'

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

    file_name ='ds-' + lop_cn.ten_lop + '.pdf'

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
    # print(list_lh)
    context = {
        "list_lh": list_lh,
    }
    return render(request, 'teacher_templates/manage_mark_template.html', context)


# def manage_detail_mark(request, tuition_id, ma_lop, mark_id):
#     ds = DiemSo.objects.get(id=mark_id)
#     detail_mark = DiemSo_ChiTiet.objects.get_or_create(mads=ds)
#     dm = detail_mark[0]
#     context = {
#         "dm": dm,
#         "ds": ds,
#         "tuition_id": tuition_id,
#         "ma_lop": ma_lop,
#     }
#     return render(request, 'teacher_templates/detail_mark_template.html', context)
#
#
# def edit_mark(request, tuition_id, ma_lop, mark_id):
#     ds = DiemSo.objects.get(id=mark_id)
#     detail_mark = DiemSo_ChiTiet.objects.get(mads=ds)
#     form = MarkForm()
#     form.fields['diem_mieng'].initial = detail_mark.diem_mieng
#     form.fields['diem_15_phut'].initial = detail_mark.diem_15_phut
#     form.fields['diem_45_phut'].initial = detail_mark.diem_45_phut
#     form.fields['diem_thi'].initial = detail_mark.diem_thi
#     context = {
#         "form": form,
#         "mark_id": mark_id,
#         "tuition_id": tuition_id,
#         "ma_lop": ma_lop,
#     }
#     return render(request, 'teacher_templates/edit_mark_template.html', context)
#
#
# def edit_mark_save(request, tuition_id, ma_lop, mark_id):
#     if request.method != "POST":
#         messages.error(request, "Invalid Method")
#         return redirect('/qldh/chinh_sua_diem_so/' + mark_id)
#     else:
#         form = MarkForm(request.POST)
#
#         if form.is_valid():
#             diem_mieng = form.cleaned_data['diem_mieng']
#             diem_15_phut = form.cleaned_data['diem_15_phut']
#             diem_45_phut = form.cleaned_data['diem_45_phut']
#             diem_thi = form.cleaned_data['diem_thi']
#             try:
#                 ds = DiemSo.objects.get(id=mark_id)
#                 dsct = DiemSo_ChiTiet.objects.get(mads=ds)
#                 dsct.diem_mieng = diem_mieng
#                 dsct.diem_15_phut = diem_15_phut
#                 dsct.diem_45_phut = diem_45_phut
#                 dsct.diem_thi = diem_thi
#                 dtb = (diem_mieng + diem_15_phut + diem_45_phut * 2 + diem_thi * 3) / 7
#                 # print(type(dtb))
#                 # print(dtb)
#                 ds.diem = round(dtb, 2)
#                 ds.trang_thai = "Đã nhập"
#                 ds.save()
#                 dsct.save()
#                 messages.success(request, "Chỉnh sửa thành công!")
#                 return redirect('/qldh/quan_ly_chi_tiet_diem_so/' + tuition_id + '/' + ma_lop + '/' + mark_id)
#             except:
#                 messages.error(request, "Chỉnh sửa không thành công!!")
#                 return redirect('/qldh/chinh_sua_diem_so/' + mark_id)
#         else:
#             return redirect('/qldh/chinh_sua_diem_so/' + mark_id)


def assessment_student(request):
    try:
        lop_cn = LopHoc.objects.get(giao_vien_chu_nhiem=request.user.username)
        ds_hs = HocSinh.objects.filter(lop=lop_cn.ma_lop)
        # nam = NamHoc.objects.get(nam_hoc=tuition.nam_hoc.nam_hoc)
        list_kq = []
        for hs in ds_hs:
            kqht = KetQuaHocTap.objects.get_or_create(mahs=hs, nam_hoc=lop_cn.nam_hoc.nam_hoc)
            # print(kqht[0])
            # print("i")
            kq = kqht[0]
            list_kq.append(kq)
    except:
        list_kq = []
        messages.error(request, "Giáo viên này không chủ nhiệm lớp nào cả")
    # print(list_kq)
    context = {
        "lop_cn": lop_cn,
        "kqht": list_kq,
    }
    return render(request, 'teacher_templates/assessment_student_template.html', context)


def edit_assessment_student(request, student_id):
    # lop_cn = LopHoc.objects.get(giao_vien_chu_nhiem=request.user.username)
    hs = HocSinh.objects.get(mahs=student_id)
    nam = NamHoc.objects.get(nam_hoc=hs.lop.nam_hoc.nam_hoc)
    ds = DiemSo.objects.filter(mahs=hs, nam_hoc=nam)
    kqht = KetQuaHocTap.objects.get(mahs=hs, nam_hoc=nam)
    list_dg = ("Xuất sắc", "Giỏi", "Khá", "Trung Bình", "Yếu", "Kém")
    tong_diem = 0.0
    for d in ds:
        tong_diem += d.diem
    diem_tb = round(tong_diem / (ds.count()), 2)
    # print(diem_tb)
    context = {
        "hs": hs,
        "ds": ds,
        "kqht": kqht,
        "list_dg": list_dg,
        "diem_tb": diem_tb,
    }
    return render(request, 'teacher_templates/edit_assessment_student_template.html', context)


def edit_assessment_student_save(request, student_id, kqht_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('assessment_student')
    else:
        xep_loai = request.POST.get('xep_loai')
        hanh_kiem = request.POST.get('hanh_kiem')
        try:
            kqht = KetQuaHocTap.objects.get(id=kqht_id)
            kqht.xep_loai = xep_loai
            kqht.hanh_kiem = hanh_kiem
            kqht.save()
            messages.success(request, "Đánh giá thành công")
            return redirect('assessment_student')
        except:
            messages.success(request, "Lỗi đánh giá")
            return redirect('/qldh/chinh_sua_danh_gia_hoc_sinh/' + student_id)


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
