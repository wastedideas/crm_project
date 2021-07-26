from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from bot_notifier import BOT_NAME
from app_crm.models import Requests
from app_users.models import Users
from app_users.forms import UserRegistration


class UserRegisterView(FormView):
    form_class = UserRegistration
    template_name = 'app_users/register.html'
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        raw_password = self.request.POST['password1']
        user = authenticate(
            username=username,
            password=raw_password,
        )
        login(self.request, user)
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'app_users/login.html'


class UserLogoutView(LogoutView):
    template_name = 'app_users/logout.html'


class PersonalAreaView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user.pk == int(self.kwargs['pk'])

    login_url = reverse_lazy('login')

    model = Users
    fields = [
        'username',
        'first_name',
        'last_name',
        'email',
    ]
    success_url = reverse_lazy('main_page')
    template_name = 'app_users/personal_area.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['users_requests'] = Requests.objects.all().filter(
            customer=self.request.user,
        )
        context['bot_name'] = BOT_NAME
        return context
