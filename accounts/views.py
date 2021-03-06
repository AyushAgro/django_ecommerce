from accounts.models import Account
from django.shortcuts import render
from .form import RegistrationForm
from .models import Account

# Create your views here.
def register(request):
  if  request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      phone_number = form.cleaned_data['phone_number']
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
    user = Account.objects.create_user()
    context = {
      'form': form
    }
    return render(request, 'accounts/register.html', context)

def login(request):
  return render(request, 'accounts/login.html')

def logout(request):
  return