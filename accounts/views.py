from datetime import timezone, datetime, timedelta
import random
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .models import OtpCode, User
from utils import send_otp_code
from .forms import UserLoginPhoneForm, VerifyCodeForm, UserRegistrationForm, LoginVerifyCodeForm, \
    UserLoginPhonePasswordForm
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
            request.session['user_information'] = {
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
        user_session = request.session.get('user_information')
        code_instance = OtpCode.objects.get(phone=user_session['phone'])
        otp_verification_expire = code_instance.created + timedelta(minutes=2)
        time_now = datetime.now(timezone.utc)

        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if time_now > otp_verification_expire:
                messages.error(request, 'code expired', 'danger')
                return redirect('accounts:verify_code')
            if cd['code'] == code_instance.code:
                User.objects.create_user(phone_number=user_session['phone'], email=user_session['email'],
                                         password=user_session['password'], full_name=user_session['full_name'])

                messages.success(request, f'Login to see your Profile', 'success')
                return redirect('accounts:user_login')
            else:
                messages.error(request, 'wrong code', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')


class UserLoginView(View):
    form_class = UserLoginPhoneForm

    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class()

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class()
        if request.method == 'POST':
            form = self.form_class(request.POST)
            random_code = random.randint(1000, 9999)
            if form.is_valid():
                cd = form.cleaned_data
                user = User.objects.filter(phone_number=cd['phone_number']).exists()
                if user:
                    send_otp_code(cd['phone_number'], random_code)
                    OtpCode.objects.create(phone=cd['phone_number'], code=random_code)
                    messages.success(request, 'we sent you a code', 'success')
                    request.session['user_login_phone'] = {'phone': cd['phone_number']}
                    return redirect('accounts:phone_verify')
                else:
                    messages.error(request, 'this phone number is invalid', 'danger')
                    return redirect('accounts:user_login')
            return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})


class PhoneVerifyLoginView(View):
    form_class = LoginVerifyCodeForm
    template_name = 'accounts/phone_verify.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user_session = request.session.get('user_login_phone')
        code_instance = OtpCode.objects.get(phone=user_session['phone'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                otp_verification_expire = code_instance.created + timedelta(minutes=2)
                time_now = datetime.now(timezone.utc)
                if time_now > otp_verification_expire:
                    messages.error(request, 'code expired', 'danger')
                    return redirect('accounts:user_login')
                else:
                    user = User.objects.get(phone_number=user_session['phone'])
                    messages.success(request, "you logged in successfully", "success")
                    login(request, user)
                    request.session.clear()
                    return render(request, 'home/home.html', {"is_active": True})
            else:
                messages.error(request, 'this code is invalid', 'danger')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out', 'success')
        return redirect('home:home')


class UserLoginWithPasswordView(View):
    form_class = UserLoginPhonePasswordForm
    template_name = 'accounts/login_with_password.html'

    def get(self, request, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'this password is incorrect', 'danger')
        return render(request, self.template_name, {'form': form})
