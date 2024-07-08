from django.shortcuts import render, redirect
from ocr.utils.bootstrap import BootStrapModelForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ocr import models
import os
# Create your views here.

from rapidocr_openvino import RapidOCR

rapid_ocr = RapidOCR()


class OcrModelForm(BootStrapModelForm):
    bootstrap_exclude_files = ['img']

    class Meta:
        model = models.Ocr
        fields = ['img']


class UserModelForm(BootStrapModelForm):
    class Meta:
        model = models.User
        fields = "__all__"


def base(request):
    return render(request, 'base.html')


def login(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'login.html', {'form': form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 去数据库校验用户名密码是否正确
        # 可以先验证有没有用户名，存在则进一步检验密码，否则不继续
        admin_object = models.User.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})
        # 用户名密码正确
        # 网站生成随机字符串；写到用户浏览器的cookie中；再写入到session 中；
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}  # 一个代码完成三个步骤
        # session 可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect('/ocr_ajax/')
    return render(request, 'login.html', {'form': form})


def login_code(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'login_code.html', {'form': form})

    form = UserModelForm(data=request.POST)
    # print(form.cleaned_data)
    if form.is_valid():
        input_code = form.cleaned_data.get('captcha')
        print(input_code)
        # 取session 中的code
        session_code = request.session.get('info')['message_code']
        print(session_code)
        # 去数据库校验用户名密码是否正确
        # 可以先验证有没有用户名，存在则进一步检验密码，否则不继续
        input_mobile = form.cleaned_data['mobile']
        admin_object = models.User.objects.filter(mobile=input_mobile).first()
        if not admin_object:
            models.User.objects.create(mobile=input_mobile)

        admin_object = models.User.objects.filter(mobile=input_mobile).first()
        # 用户名密码正确
        if input_code != session_code:
            form.add_error("captcha", "验证码不正确")
            return render(request, 'login_code.html', {'form': form})
        # 网站生成随机字符串；写到用户浏览器的cookie中；再写入到session 中；
        request.session['info'] = {'id': admin_object.id, 'mobile': admin_object.mobile}  # 一个代码完成三个步骤
        # session 可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect('/ocr/')
    return render(request, 'login_code.html', {'form': form})


def send_message(request):
    """发送短信验证码"""
    import urllib.parse
    import urllib.request
    import random
    # 获取ajax的get方法发送过来的手机号码
    mobile = request.GET.get('mobile')
    # 接口地址
    url = 'http://106.ihuyi.com/webservice/sms.php?method=Submit'

    message_code = ''
    for i in range(4):
        i = random.randint(0, 9)
        message_code += str(i)

    # 定义请求的数据
    values = {
        'account': 'xxxxxxxx',
        'password': 'xxxxxxxxxxxx',
        'mobile': mobile,
        'content': '您的验证码是：%s。请不要把验证码泄露给其他人。' % (message_code),
        'format': 'json',
    }
    print(values)

    # # 将数据进行编码
    # data = urllib.parse.urlencode(values).encode(encoding='UTF8')
    #
    # # 发起请求
    # req = urllib.request.Request(url, data)
    # response = urllib.request.urlopen(req)
    # res = response.read()

    # 把验证码放进session中
    request.session['info'] = {'message_code': message_code}

    # request.session['message_code'] = message_code
    # print(eval(res.decode("utf8")))
    # 使用eval把字符串转为json数据返回
    # return JsonResponse(eval(res.decode("utf8")))
    return JsonResponse({'msg': '提交成功','code':message_code})


def logout(request):
    request.session.clear()
    return redirect('/login_code/')




@csrf_exempt
def ocr(request):
    if request.method == 'GET':
        form = OcrModelForm()
        return render(request, 'ocr_ajax.html', {'form': form})
    form = OcrModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 固定设置管理员id
        # form.instance.admin_id = 当前登录系统管理的id
        form.instance.mobile_id = request.session['info']['id']
        obj = form.save()

        img_url = obj.img.url
        print(type(img_url))
        print(img_url)
        if img_url.endswith('.png') or img_url.endswith('.jpg'):
            processed_result = process_image(obj.img.path)
        else:
            processed_result = '请上传图片文件！'
            os.remove(obj.img.path) # 防止用户上传太大的非图片文件占用内存，所以直接删掉
        # print(processed_result)
        return JsonResponse({'status': True, 'result': processed_result, 'img_url': img_url})
    return JsonResponse({'status': False, 'error': form.errors})


def process_image(file_path):
    final_result, elapse_part = rapid_ocr(file_path)
    if final_result:
        result_text = "\n".join([res[1] for res in final_result])
        return result_text
    return "未识别到文字，请更换图片！"
