from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView
from django.contrib.auth import login

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "تم إنشاء الحساب بنجاح 🎉، أهلاً بك!")
            return redirect('home_page')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

from django.utils.translation import get_language


class CustomLoginView(LoginView):
    def get_success_url(self):
        lang = get_language()
        if self.request.user.is_superuser:
            return f'/{lang}/dashboard/'
        else:
            return f'/{lang}/'