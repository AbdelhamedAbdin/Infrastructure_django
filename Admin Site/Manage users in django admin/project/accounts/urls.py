from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

app_name = 'accounts'


class Login(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('accounts:profile', args=[self.request.user.id])

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'username or password are invalid. please try again.', extra_tags='validate_form')
        return redirect('accounts:login')


urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html', next_page=reverse_lazy('accounts:login')), name='logout'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('delete/<int:id>/', views.delete_user, name='delete_user'),
]
