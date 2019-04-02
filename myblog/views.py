# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from myblog import models
from django import views
from django.utils.safestring import mark_safe
from utils.Page import PageHelper
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
# from django.contrib.sessions.backends import

def userInfo(req):

    if req.method=="POST":
        u=req.POST.get("username", None)
        s=req.POST.get("sex", None)
        e=req.POST.get("email", None)

        models.UserInfo.objects.create(
            username=u,
            sex=s,
            email=e,
        )
    user_list = models.UserInfo.objects.all()
    return render(req, "index.html", {"user_list": user_list})

# def outer(func):
#     def inner(request, *args, **kwargs):
#         print(request.method)
#         return func(request, *args, **kwargs)
#     return inner

# CBV
class Login(views.View):

    def dispatch(self, request, *args, **kwargs):
        print('要执行父类 dispatch 方法')
        # 调用父类方法
        ret = super(Login, self).dispatch(request, *args, **kwargs)
        print('执行完了父类 dispatch 方法')
        return ret

    # @method_decorator(outer())
    def get(self, request, *args, **kwargs):
        print(request.method, 'GET')
        return render(request, 'login.html', {'msg': ''})

    def post(self, request, *args, **kwargs):
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        # c = models.Administrator.objects.filter(username=user, password=pwd).count()
        # if c:
        if user == 'root' and pwd == '123':
            request.session['is_login'] = True
            request.session['username'] = user
            rep = redirect('/index1/')
            return rep
        else:
            message = 'invalid username or password'
            return render(request, 'login.html', {'msg': message})



# def login(request):
#     message = ''
#     v = request.session
#     print(type(v))
#
#     if request.method == 'POST':
#         user = request.POST.get('username')
#         pwd = request.POST.get('password')
#
#         # c = models.Administrator.objects.filter(username=user, password=pwd).count()
#         #
#         # if c:
#         if user == 'root' and pwd == '123':
#             request.session['is_login'] = True
#             request.session['username'] = user
#             rep = redirect('/index1.html')
#             return rep
#         else:
#             message = 'invalid username or password'
#
#     obj = render(request, 'login.html', {"msg": message})
#     return obj

def index1(request):
    cur_user = request.session.get('username')
    return render(request, 'index1.html', {'username': cur_user})

# def logout(request):
#     request.session.clear()
#     return redirect('/login.html')
#
# def auth(func):
#     def inner(request, *args, **kwargs):
#         is_login = request.session.get('is_login')
#         if is_login:
#             return func(request, *args, **kwargs)
#         else:
#             return redirect('login.html')
#     return inner()
#
#


def handle_classes(request):
    if request.method == 'GET':
        cur_page = int(request.GET.get('page', 1))
        cur_user = request.session.get('username')
        total = models.Classes.objects.all().count()
        obj = PageHelper(total, cur_page, '/classes', 30)
        page_str = obj.page_str()

        cls_list = models.Classes.objects.all()[obj.db_start:obj.db_end]
        return render(request, 'classes.html', {'username': cur_user, 'cls_obj': cls_list, 'page_list': mark_safe(page_str)})
    elif request.method == 'POST':
        # form 表单提交的处理方式
        '''
        print(111111)
        caption = request.POST.get('caption', None)
        if caption:
            models.Classes.objects.create(caption=caption)
        return redirect('/classes/')
        '''

        # Ajax
        import json
        response_dict = {'info': 'add', 'status': True, 'error': None, 'data': 'None'}

        caption = request.POST.get('caption', None)
        print(caption)
        if caption:
            response_dict['data'] = {'nid': 1, 'caption': 2}
            obj = models.Classes.objects.create(caption=caption)
            print(obj.id, obj.caption)
            response_dict['error'] = 'success'
            response_dict['data'] = {'nid': obj.id, 'caption': obj.caption}
        else:
            response_dict['status'] = False
            response_dict['error'] = '标题不能为空'
        return HttpResponse(json.dumps(response_dict))

def handle_add_classes(request):
    msg = ''
    cur_user = request.session.get('username')
    if request.method == 'GET':
        return render(request, 'add_classes.html', {'username': cur_user, 'message': msg})
    elif request.method == 'POST':
        caption = request.POST.get('caption', None)
        if caption:
            msg = 'success'
            models.Classes.objects.create(caption=caption)
        else:
            msg = '标题不能为空'
            return render(request, 'add_classes.html', {'username': cur_user, 'message': msg})
        return redirect('/classes')
    else:
        return redirect('/index1/')

def handle_edit_class(request):
    if request.method == "GET":
        nid = request.GET.get("nid")
        obj = models.Classes.objects.filter(id=nid).first()
        return render(request, 'edit_class.html', {"obj": obj})
    elif request.method == "POST":
        nid = request.POST.get("nid")
        caption = request.POST.get("caption")
        models.Classes.objects.filter(id=nid).update(caption=caption)
        return redirect("/classes/")
    else:
        return redirect("/index1/")

def handle_up_class(request):
    # AJAX
    import json
    data_response = {'info': 'up', 'status': False, 'error': None, 'data': None}
    nid = request.POST.get('id', None)
    caption = request.POST.get('caption', None)
    print(nid, caption)
    if caption:
        models.Classes.objects.filter(id=nid).update(caption=caption)
        data_response['status'] = True
        data_response['data'] = {'nid': nid, 'caption': caption}
    return HttpResponse(json.dumps(data_response))

def handle_del_class(request):
    nid = request.POST.get("nid")
    models.Classes.objects.filter(id=nid).delete()
    cur_user = request.session.get('username')
    return redirect('/classes/')


def handle_get_all_classes(request):
    import json
    response_data = {"status": False, "data": None, "error": "no class can be selected"}
    class_all = models.Classes.objects.values("id", "caption")
    class_list = list(class_all)
    print(class_list)
    if class_list:
        response_data["status"] = True
        response_data["data"] = class_list
        print(type(class_list))
        response_data['error'] = ""
    return HttpResponse(json.dumps(response_data))



def handle_student(request):
    cur_user = request.session.get('username')
    return render(request, 'student.html', {'username': cur_user})


def handle_teacher(request):
    cur_user = request.session.get('username')
    # teacher_list = models.Teacher.objects.all()
    teacher_list = models.Teacher.objects.values('id', 'name', 'cls__id', 'cls__caption')
    teacher_set = {}
    for item in teacher_list:
        if item["id"] in teacher_set:
            cls_dict = {"cls__id": item["cls__id"], "cls__caption": item["cls__caption"]}
            teacher_set[item["id"]]["cls"].append(cls_dict)
        else:
            cls_list = [{"cls__id": item["cls__id"], "cls__caption": item["cls__caption"]}]
            teacher_set[item["id"]] = {'name': item["name"], "cls": cls_list}
    return render(request, 'teacher.html', {'username': cur_user, "teacher_list": teacher_set})


def handle_add_teacher(request):
    caption = request.POST.get

def handle_del_tea_cls(request):
    import json
    resp_data = {"status": False, "error": None}
    nid = request.POST.get('nid')
    cls_id = request.POST.get("cls_id")
    print(nid, cls_id)
    obj = models.Teacher.objects.filter(id=nid).first()
    obj.cls.remove(*cls_id)
    resp_data["status"] = True
    return HttpResponse(json.dumps(resp_data))





