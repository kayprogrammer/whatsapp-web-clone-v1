from django.shortcuts import redirect, render
from django.views import View

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
            form.save()
        print(form.errors)
        return redirect('/accounts/register/')