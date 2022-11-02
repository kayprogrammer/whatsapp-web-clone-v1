from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout

from . forms import CustomUserCreationForm

# Create your views here.

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()

        context = {'form': form}
        return render(request, "accounts/register.html", context)

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return JsonResponse(
                {
                    'user': {'name': user.name, 'email': user.email, 'phone': user.phone},
                    'success': "Registration successful"
                }
            )
        else:
            print(form.errors.as_json())
            return JsonResponse({'errors': form.errors.as_json()})

class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "accounts/login.html")

    def post(self, request, *args, **kwargs):
        email_or_phone = request.POST.get('email_or_phone')
        password = request.POST.get('password')
        user = authenticate(request, username=email_or_phone, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'})
