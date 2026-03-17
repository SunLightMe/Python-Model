from django.shortcuts import render, redirect
from app01 import models


def depart_list(request):
    """部门表"""
    queryset = models.Department.objects.all()
    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    """增加部门"""
    if request.method == "GET":
        return render(request, 'depart_add.html')

    # 获取用户post提交的参数
    title = request.POST.get('title')

    # 增加到数据库
    models.Department.objects.create(title=title)

    # 重定向到部门页面
    return redirect("/depart/list")


def depart_delete(request):
    """删除部门"""
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart/list')


def depart_edit(request, nid):
    if request.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {'row_object': row_object})

    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list')


def user_list(request):
    """用户管理 """
    row_object = models.Userinfo.objects.all()
    return render(request, 'user_list.html', {'queryset': row_object})


def user_add(request):
    """增加用户"""
    if request.method == 'GET':
        context = {
            'gender_choices': models.Userinfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)

    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender_id = request.POST.get('gd')
    depart_id = request.POST.get('dp')

    models.Userinfo.objects.create(name=user, password=pwd, age=age,
                                   account=account, create_time=ctime,
                                   gender=gender_id, depart_id=depart_id)
    return redirect('/user/list/')


# -----------------model-------------------

from django import forms


class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3, label='用户名')

    password = forms.CharField(min_length=3, label='密码')

    class Meta:
        model = models.Userinfo
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


def user_model_add(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_model_add.html', {'form': form})

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    else:
        return render(request, 'user_model_add.html', {'form': form})


def user_edit(request, nid):
    """编辑用户"""
    row_object = models.Userinfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})
    else:
        form = UserModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('/user/list/')
        return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    models.Userinfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


'''-------- 靓号管理----------'''


def pretty_list(request):
    queryset = models.PrettyNum.objects.all().order_by('-level')
    return render(request, 'pretty_list.html', {'queryset': queryset})


from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class PrettyModelForm(forms.ModelForm):
    # 验证方式1：
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']
        # exclude = ['level']
        # fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

    #方法2
    # def clean_mobile(self):
    #     txt_mobile = self.cleaned_data['mobile']
    #     if len(txt_mobile) != 11:
    #         raise ValidationError('格式错误')
    #     return txt_mobile

def pretty_add(request):
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form': form})
