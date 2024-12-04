from datetime import timezone,datetime,timedelta
import random


from django.shortcuts import render, redirect
from django.views import View
from .models import OtpCode, User
from utils import send_otp_code
from .forms import UserCreationForm, VerifyCodeForm, UserRegistrationForm
from django.contrib import messages


# Create your views here.
class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone=form.cleaned_data['phone_number'], code=random_code)
            request.session['user_registration_info'] = {
                'phone': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password']

            }
            messages.success(request, 'we sent you a code', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name = 'accounts/verify.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user_session = request.session.get('user_registration_info')
        code_instance = OtpCode.objects.get(phone=user_session['phone'])
        otp_verification_expire =code_instance.created + timedelta(minutes=2)
        time_now = datetime.now(timezone.utc)

        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if time_now > otp_verification_expire:
                messages.error(request, 'code expired', 'danger')
                code_instance.delete()
                return redirect('accounts:verify_code')
            if cd['code'] == code_instance.code:
                User.objects.create_user(phone_number=user_session['phone'], email=user_session['email'],
                                         password=user_session['password'], full_name=user_session['full_name'])
                code_instance.delete()
                messages.success(request, 'your account created successfully', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'wrong code', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')
