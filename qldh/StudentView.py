from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CustomUser, TrinhDoHocVan, PhongHoc, LopHoc, MonHoc, NamHoc, GiaoVien, HocSinh, GiangDay, DiemSo, KetQuaHocTap


def student_home(request):
    return render(request, 'student_templates/home_content.html')


def view_classroom(request):
    lop = LopHoc.objects.get(ma_lop=request.user.hocsinh.lop.ma_lop)
    context = {
        "lop": lop,
    }
    return render(request, 'student_templates/view_classroom_template.html', context)


def view_personal_mark(request):
    lop = LopHoc.objects.get(ma_lop=request.user.hocsinh.lop.ma_lop)
    nam = lop.nam_hoc.nam_hoc
    nam_hoc = lop.nam_hoc.mo_ta
    list_hk = ["Học Kỳ I", "Học Kỳ II"]
    ds = DiemSo.objects.filter(mahs=request.user.username, nam_hoc=nam)
    context = {
        "ds": ds,
        "nam_hoc": nam_hoc,
        "hoc_ky": list_hk,
    }
    return render(request, 'student_templates/view_personal_mark_template.html', context)


@csrf_exempt
def student_get_mark(request):
    if request.accepts("application/json") and request.method == "POST":
        nam_hoc = request.POST.get('nam_hoc')
        hoc_ky = request.POST.get('hoc_ky')
        nam = NamHoc.objects.get(mo_ta=nam_hoc)
        try:
            if hoc_ky == 'all':
                diem_so = DiemSo.objects.filter(mahs=request.user.username, nam_hoc=nam)
            else:
                diem_so = DiemSo.objects.filter(mahs=request.user.username, nam_hoc=nam, hoc_ky=hoc_ky)
            list_data = []
            for ds in diem_so:
                small_data = {"mon": ds.mon.ten_mon,"hoc_ky": ds.hoc_ky, "diem_mieng":ds.diemso_chitiet.diem_mieng, "diem_15_phut":ds.diemso_chitiet.diem_15_phut, "diem_45_phut":ds.diemso_chitiet.diem_45_phut, "diem_thi":ds.diemso_chitiet.diem_thi, "diem_tb":ds.diem, "trang_thai":ds.trang_thai}
                list_data.append(small_data)
            # print(list_data)
            return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)
        except:
            return JsonResponse({"error": ""}, status=400)
    return JsonResponse({"error": ""}, status=400)


def view_result_study(request):
    lop = LopHoc.objects.get(ma_lop=request.user.hocsinh.lop.ma_lop)
    nam = lop.nam_hoc.nam_hoc
    ds = DiemSo.objects.filter(mahs=request.user.username, nam_hoc=nam)
    kqht = KetQuaHocTap.objects.get(mahs=request.user.username, nam_hoc=nam)
    tong_diem = 0.0
    for d in ds:
        tong_diem += d.diem
    diem_tb = round(tong_diem / (ds.count()), 2)
    so_mon = ds.count()
    context = {
        "diem_tb": diem_tb,
        "kqht": kqht,
        "so_mon": so_mon,
    }
    return render(request, 'student_templates/view_result_study_template.html', context)


def profile_student(request):
    return render(request, 'student_templates/profile_student_template.html')


def change_password_student(request):
    return render(request, 'student_templates/change_password_template.html')


def change_password_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('change_password_student')
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
                return redirect('change_password_student')
                # print(request.user.check_password(old_password))
            else:
                # print(request.user.check_password(old_password))
                messages.error(request, "Mật khẩu cũ không đúng")
                return redirect('change_password_student')
        else:
            messages.error(request, "Mật khẩu mới không trùng nhau")
            return redirect('change_password_student')
