from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import User, Profile


def home(request):
    return render(request, 'app1/index.html')


# Register
def register(request):
    form = RegisterForm
    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app1:login')
    return render(request, 'app1/register.html', {'forms': form})


# Profile View
def profile(request, id=None):
    context = {}
    try:
        user = User.objects.get(id=id)
        user = Profile.objects.get(user__email=user)
        context['userprofile'] = user
    except User.DoesNotExist:
        error = 'This User Does Not Exist'
        return render(request, 'page404.html', {'error': error})
    return render(request, 'app1/profile.html', context)


# Delete User
def delete_user(request, id=None):
    if 'delete_user' in request.POST and id is not None:
        User.objects.get(id=id).delete()
    return redirect('app1:register')
