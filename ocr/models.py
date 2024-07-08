from django.db import models
from django.utils import timezone
# Create your models here.


# class User(models.Model):
#     """"""
#     username = models.CharField(verbose_name='用户名', max_length=32)
#     password = models.CharField(verbose_name='密码', max_length=64)
#
#     def __str__(self): # html上输出时让它显示值而不是显示对象
#         return self.username
class User(models.Model):
    """"""
    mobile = models.CharField(verbose_name='手机号', max_length=11,)
    captcha = models.CharField(verbose_name='验证码', max_length=4, null=True)
    def __str__(self): # html上输出时让它显示值而不是显示对象
        return self.mobile

class Ocr(models.Model):
    create_time = models.DateTimeField(verbose_name='日期',auto_now=True)
    img = models.FileField(verbose_name='图片',max_length=128,upload_to='ocr/')
    mobile = models.ForeignKey(verbose_name='手机号',to='User',on_delete=models.CASCADE)

