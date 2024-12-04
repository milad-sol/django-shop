import random

from django.shortcuts import render,redirect
from django.views import View
from .models import OtpCode
from utils import send_otp_code
from .forms import UserCreationForm,VerifyCodeForm
from django.contrib import messages

# Create your views here.
class UserRegisterView(View):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form ': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone=form.cleaned_data['phone_number'], otp_code=random_code)
            request.session['user_registration_ingo'] = {
                'phone': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password']

            }
            messages.success(request,'we sent you a code','success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form ': form})


class UserRegisterVerifyCodeView(View):
    def get (self,request):
        pass

    def post(self,request):
        pass