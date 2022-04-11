from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={"required": "请填写用户名"})
    password = forms.CharField(required=True, error_messages={"required": u"请填写密码"})


class ChangePwdForm(forms.Form):
    """
    管理员用户修改用户列表中的用户密码
    """
    # def __init__(self, *args, **kwargs):
    #     super(AdminPasswdChangeForm, self).__init__(*args, **kwargs)

    password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": u"密码不能为空"
        })

    confirm_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": u"确认密码不能为空"
        })

    def clean(self):
        cleaned_data = super(ChangePwdForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("两次密码输入不一致")


class UploadImagForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image']