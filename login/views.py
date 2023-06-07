from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
     get_user_model, logout as auth_logout,
)
from .forms import UserCreateForm,UserChangeForm
from .models import User
from django.views.generic import FormView

<<<<<<< HEAD
# Create your views here.

class views():
    
    def signup_view():
        pass
    
    def signin_view():
        pass    
    
    def signout_view():
        pass
    
    
=======
User = get_user_model()

class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login:profile')
    template_name = 'login/signup.html'


class ProfileView(LoginRequiredMixin, generic.View):

    def get(self, *args, **kwargs):
        return render(self.request,'login/profile.html')   
    


class DeleteView(LoginRequiredMixin, generic.View):

    def get(self, *args, **kwargs):
        user = User.objects.get(email=self.request.user.email)
        user.is_active = False
        user.save()
        auth_logout(self.request)
        return render(self.request,'login/delete_complete.html')

class UserChangeView(LoginRequiredMixin, FormView):
    template_name = 'login/change.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('login:profile')
    
    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'username' : self.request.user.username,
            'nickname' : self.request.user.nickname,
            'grade' : self.request.user.grade,
        })        
        return kwargs
>>>>>>> ed179e374f379d614c5feb07343f6dc59a9f6f88
