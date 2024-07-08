from django import forms


class Bootstrap:
    bootstrap_exclude_files =[]
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        # 循环modelform中的所有字段，给每个字段的插件设置
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_files:
                continue
            # 字段中有属性，保留原来的属性，没有属性才增加
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs ={
                    'class': 'form-control',
                    'placeholder': field.label,
                }

class BootStrapModelForm(Bootstrap, forms.ModelForm):
    pass

