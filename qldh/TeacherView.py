from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CustomUser, TrinhDoHocVan, PhongHoc, LopHoc, MonHoc, NamHoc, GiaoVien, HocSinh, GiangDay, DiemSo_ChiTiet, DiemSo, KetQuaHocTap
from .forms import MarkForm


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
    giang_day = GiangDay.objects.filter(magv=request.user.username)
    list_hk = ["Học Kỳ I", "Học Kỳ II"]
    nam_hoc = NamHoc.objects.all()
    context = {
        "dsgd": giang_day,
        "hoc_ky": list_hk,
        "nam_hoc": nam_hoc,
    }
    return render(request, 'teacher_templates/view_tuition_tempale.html', context)


@csrf_exempt
def teacher_get_tuition(request):
    if request.accepts("application/json") and request.method == "POST":
        nam_hoc = request.POST.get('nam_hoc')
        hoc_ky = request.POST.get('hoc_ky')
        try:
            if nam_hoc == 'all' and hoc_ky == 'all':
                tuition = GiangDay.objects.filter(magv=request.user.username)
            elif nam_hoc == 'all':
                tuition = GiangDay.objects.filter(magv=request.user.username, hoc_ky=hoc_ky)
            elif hoc_ky == 'all':
                nh = NamHoc.objects.get(nam_hoc=nam_hoc)
                tuition = GiangDay.objects.filter(magv=request.user.username, nam_hoc=nh)
            else:
                nh = NamHoc.objects.get(nam_hoc=nam_hoc)
                tuition = GiangDay.objects.filter(magv=request.user.username, nam_hoc=nh, hoc_ky=hoc_ky)
            # print(hoc_sinh)
            list_data = []
            for gd in tuition:
                small_data = {"id": gd.id,"ma_lop": gd.ma_lop.ma_lop, "mon":gd.magv.day_mon.ten_mon, "lop":gd.ma_lop.ten_lop, "hoc_ky": gd.hoc_ky, "nam_hoc":gd.nam_hoc.mo_ta}
                list_data.append(small_data)
            # print(list_data)
            return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)
        except:
            return JsonResponse({"error": ""}, status=400)
    return JsonResponse({"error": ""}, status=400)


# def view_detail_tuition(request, tuition_id):
#     try:
#         list_detail = GiangDay_ChiTiet.objects.filter(magd=tuition_id)
#     except:
#         list_detail = []
#     context = {
#         "gdct": list_detail,
#     }
#     return render(request, 'teacher_templates/view_detail_tuition_template.html', context)


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


def manage_mark(request, tuition_id, ma_lop):
    ds_hs = HocSinh.objects.filter(lop=ma_lop)
    lop = LopHoc.objects.get(ma_lop=ma_lop)
    tuition = GiangDay.objects.get(id=tuition_id)
    nam = NamHoc.objects.get(nam_hoc=tuition.nam_hoc.nam_hoc)
    mon = MonHoc.objects.get(ma_mon=tuition.magv.day_mon.ma_mon)
    hoc_ky = tuition.hoc_ky
    student_list = []
    for hs in ds_hs:
        student_mark = DiemSo.objects.get_or_create(mahs=hs, nam_hoc=nam, mon=mon, hoc_ky=hoc_ky)
        sm = student_mark[0]
        student_list.append(sm)
    # print(student_list)
    context = {
        "ds_hs": student_list,
        "lop": lop,
        "tuition": tuition,
    }
    return render(request, 'teacher_templates/manage_mark_template.html', context)


def manage_detail_mark(request, tuition_id, ma_lop, mark_id):
    ds = DiemSo.objects.get(id=mark_id)
    detail_mark = DiemSo_ChiTiet.objects.get_or_create(mads=ds)
    dm = detail_mark[0]
    context = {
        "dm": dm,
        "ds": ds,
        "tuition_id": tuition_id,
        "ma_lop": ma_lop,
    }
    return render(request, 'teacher_templates/detail_mark_template.html', context)


def edit_mark(request, tuition_id, ma_lop, mark_id):
    ds = DiemSo.objects.get(id=mark_id)
    detail_mark = DiemSo_ChiTiet.objects.get(mads=ds)
    form = MarkForm()
    form.fields['diem_mieng'].initial = detail_mark.diem_mieng
    form.fields['diem_15_phut'].initial = detail_mark.diem_15_phut
    form.fields['diem_45_phut'].initial = detail_mark.diem_45_phut
    form.fields['diem_thi'].initial = detail_mark.diem_thi
    context = {
        "form": form,
        "mark_id": mark_id,
        "tuition_id": tuition_id,
        "ma_lop": ma_lop,
    }
    return render(request, 'teacher_templates/edit_mark_template.html', context)


def edit_mark_save(request, tuition_id, ma_lop, mark_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('/qldh/chinh_sua_diem_so/' + mark_id)
    else:
        form = MarkForm(request.POST)

        if form.is_valid():
            diem_mieng = form.cleaned_data['diem_mieng']
            diem_15_phut = form.cleaned_data['diem_15_phut']
            diem_45_phut = form.cleaned_data['diem_45_phut']
            diem_thi = form.cleaned_data['diem_thi']
            try:
                ds = DiemSo.objects.get(id=mark_id)
                dsct = DiemSo_ChiTiet.objects.get(mads=ds)
                dsct.diem_mieng = diem_mieng
                dsct.diem_15_phut = diem_15_phut
                dsct.diem_45_phut = diem_45_phut
                dsct.diem_thi = diem_thi
                dtb = (diem_mieng + diem_15_phut + diem_45_phut*2 + diem_thi*3)/7
                # print(type(dtb))
                # print(dtb)
                ds.diem = round(dtb, 2)
                ds.trang_thai = "Đã nhập"
                ds.save()
                dsct.save()
                messages.success(request, "Chỉnh sửa thành công!")
                return redirect('/qldh/quan_ly_chi_tiet_diem_so/' + tuition_id + '/' + ma_lop + '/' + mark_id)
            except:
                messages.error(request, "Chỉnh sửa không thành công!!")
                return redirect('/qldh/chinh_sua_diem_so/' + mark_id)
        else:
            return redirect('/qldh/chinh_sua_diem_so/' + mark_id)


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
    diem_tb = round(tong_diem/(ds.count()), 2)
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
