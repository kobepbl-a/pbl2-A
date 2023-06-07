from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
User = get_user_model()


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        """
        if User.USERNAME_FIELD == 'email':
            fields = ('email',)
        else:
        """
        fields = ('username','nickname', 'email')
                
                
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs.update({'placeholder': '8文字以上のパスワード',})
        self.fields['password2'].widget.attrs.update({'placeholder': '8文字以上のパスワード',})

class UserChangeForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'nickname',
            'grade',
            #'icon'
        ]

    def __init__(self,nickname=None, username=None,grade=None, *args, **kwargs):
        #kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # ユーザーの更新前情報をフォームに挿入
        if nickname:
            self.fields['nickname'].widget.attrs['value'] = nickname
        if username:
            self.fields['username'].widget.attrs['value'] = username
            
        if grade:
            self.fields['grade'].widget.attrs['value'] = grade

    def update(self, user):
        user.username = self.cleaned_data['username']
        user.nickname = self.cleaned_data['nickname']
        user.grade = self.cleaned_data['grade']
        #if self.cleaned_data['icon']:
         #   user.icon = self.cleaned_data['icon']        
        user.save()