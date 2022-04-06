from django.urls import path, include
from . import views
from . import AdminView, TeacherView, StudentView

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('admin_home/', AdminView.admin_home, name="admin_home"),
    path('check_email_exist/', AdminView.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', AdminView.check_username_exist, name="check_username_exist"),
    path('download_excel/<file_name>', AdminView.download_excel, name="download_excel"),

    path('quan_ly_giao_vien/', AdminView.manage_teacher, name="manage_teacher"),
    path('admin_get_teacher/', AdminView.admin_get_teacher, name="admin_get_teacher"),
    path('them_moi_giao_vien_xls/', AdminView.add_teacher_from_xls, name="add_teacher_from_xls"),
    path('luu_them_moi_giao_vien/', AdminView.add_teacher_save, name="add_teacher_save"),
    path('chinh_sua_giao_vien/<magv>/', AdminView.edit_teacher, name="edit_teacher"),
    path('luu_chinh_sua_giao_vien/', AdminView.edit_teacher_save, name="edit_teacher_save"),
    path('xoa_giao_vien/<magv>/', AdminView.delete_teacher, name="delete_teacher"),
    path('quan_ly_phong_hoc/', AdminView.manage_study_room, name="manage_study_room"),
    path('admin_get_classroom/', AdminView.admin_get_classroom, name="admin_get_classroom"),
    path('them_moi_phong_hoc_xls/', AdminView.add_study_room_from_xls, name="add_study_room_from_xls"),
    path('luu_them_moi_phong_hoc/', AdminView.add_study_room_save, name="add_study_room_save"),
    path('chinh_sua_phong_hoc/<ma_phong>/', AdminView.edit_study_room, name="edit_study_room"),
    path('luu_chinh_sua_phong_hoc/', AdminView.edit_study_room_save, name="edit_study_room_save"),
    path('xoa_phong_hoc/<ma_phong>/', AdminView.delete_study_room, name="delete_study_room"),
    path('quan_ly_lop_hoc/', AdminView.manage_classroom, name="manage_classroom"),
    path('them_moi_lop_hoc_xls/', AdminView.add_classroom_from_xls, name="add_classroom_from_xls"),
    path('luu_them_moi_lop_hoc/', AdminView.add_classroom_save, name="add_classroom_save"),
    path('chinh_sua_lop_hoc/<ma_lop>/', AdminView.edit_classroom, name="edit_classroom"),
    path('luu_chinh_sua_lop_hoc/', AdminView.edit_classroom_save, name="edit_classroom_save"),
    path('xoa_lop_hoc/<ma_lop>/', AdminView.delete_classroom, name="delete_classroom"),

    path('admin_get_student/', AdminView.admin_get_student, name="admin_get_student"),
    path('quan_ly_hoc_sinh/', AdminView.manage_student, name="manage_student"),
    path('them_moi_hoc_sinh_xls/', AdminView.add_student_from_xls, name="add_student_from_xls"),
    path('luu_them_moi_hoc_sinh/', AdminView.add_student_save, name="add_student_save"),
    path('chinh_sua_hoc_sinh/<mahs>/', AdminView.edit_student, name="edit_student"),
    path('luu_chinh_sua_hoc_sinh/', AdminView.edit_student_save, name="edit_student_save"),
    path('xoa_hoc_sinh/<mahs>/', AdminView.delete_student, name="delete_student"),

    path('get_teacher/', AdminView.get_teacher, name="get_teacher"),

    path('quan_ly_giang_day/', AdminView.manage_tuition, name="manage_tuition"),
    path('them_moi_giang_day_ajax/', AdminView.them_moi_giang_day, name="them_moi_giang_day_ajax"),
    path('chinh_sua_lop_giang_day_ajax/', AdminView.chinh_sua_lop_giang_day, name="chinh_sua_lop_giang_day_ajax"),
    path('xoa_giang_day_ajax/', AdminView.xoa_giang_day, name="xoa_giang_day_ajax"),

    path('admin_get_tuition_new/', AdminView.get_tuition, name="get_tuition"),
    path('quan_ly_mon_hoc/', AdminView.manage_subject, name="manage_subject"),
    path('kiem_tra_ma_mon/', AdminView.kiem_tra_ma_mon, name="kiem_tra_ma_mon"),
    path('kiem_tra_ten_mon/', AdminView.kiem_tra_ten_mon, name="kiem_tra_ten_mon"),
    path('them_moi_mon_hoc_xls/', AdminView.add_subject_from_xls, name="add_subject_from_xls"),
    path('luu_them_moi_mon_hoc/', AdminView.add_subject_save, name="add_subject_save"),
    path('chinh_sua_mon_hoc/<ma_mon>/', AdminView.edit_subject, name="edit_subject"),
    path('luu_chinh_sua_mon_hoc/<ma_mon>/', AdminView.edit_subject_save, name="edit_subject_save"),
    path('xoa_mon_hoc/<ma_mon>/', AdminView.delete_subject, name="delete_subject"),

    # URLS for GiaoVien
    path('teacher_get_tuition/', TeacherView.teacher_get_tuition, name="teacher_get_tuition"),
    path('teacher_home/', TeacherView.teacher_home, name="teacher_home"),
    path('danh_sach_giang_day/', TeacherView.view_tuition, name="view_tuition"),
    path('tai_xuong_tkb/', TeacherView.tkb_gv_pdf, name="tkb_gv_pdf"),
    path('danh_sach_hoc_sinh_chu_nhiem/', TeacherView.view_student, name="view_student"),
    path('quan_ly_diem_so/<tuition_id>/<ma_lop>/', TeacherView.manage_mark, name="manage_mark"),
    path('quan_ly_chi_tiet_diem_so/<tuition_id>/<ma_lop>/<mark_id>/', TeacherView.manage_detail_mark,
         name="manage_detail_mark"),
    path('chinh_sua_diem_so/<tuition_id>/<ma_lop>/<mark_id>/', TeacherView.edit_mark, name="edit_mark"),
    path('luu_chinh_sua_diem_so/<tuition_id>/<ma_lop>/<mark_id>/', TeacherView.edit_mark_save, name="edit_mark_save"),
    path('danh_gia_hoc_sinh/', TeacherView.assessment_student, name="assessment_student"),
    path('chinh_sua_danh_gia_hoc_sinh/<student_id>/', TeacherView.edit_assessment_student,
         name="edit_assessment_student"),
    path('luu_danh_gia_hoc_sinh/<student_id>/<kqht_id>/', TeacherView.edit_assessment_student_save,
         name="edit_assessment_student_save"),
    path('thong_tin_ca_nhan/', TeacherView.profile_teacher, name="profile_teacher"),
    path('doi_mat_khau/', TeacherView.change_password, name="change_password"),
    path('luu_doi_mat_khau/', TeacherView.change_password_save, name="change_password_save"),

    # URLS for HocSinh
    path('student_home/', StudentView.student_home, name="student_home"),
    path('student_get_mark/', StudentView.student_get_mark, name="student_get_mark"),
    path('xem_thong_tin_lop_hoc/', StudentView.view_classroom, name="view_classroom"),
    path('xem_diem_so_ca_nhan/', StudentView.view_personal_mark, name="view_personal_mark"),
    path('xem_ket_qua_hoc_tap/', StudentView.view_result_study, name="view_result_study"),
    path('thong_tin_ca_nhan_hoc_sinh/', StudentView.profile_student, name="profile_student"),
    path('doi_mat_khau_hoc_sinh/', StudentView.change_password_student, name="change_password_student"),
    path('luu_doi_mat_khau_hoc_sinh/', StudentView.change_password_student_save, name="change_password_student_save"),
]
