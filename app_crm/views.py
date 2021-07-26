import random
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from enhanced_cbv.views import ListFilteredView
from app_crm.models import Requests
from app_crm.filters import RequestsFilter
from app_crm.forms import EditRequestForm
from app_users.models import Users


class RequestCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'app_crm.add_requests'
    login_url = reverse_lazy('login')

    model = Requests
    fields = ['title', 'text', 'request_type']
    template_name = 'app_crm/create_or_edit_request.html'
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        form.instance.customer = self.request.user
        form.instance.worker = random.choice(
            Users.objects.filter(
                groups__name='workers',
            )
        )
        form.save()
        return super().form_valid(form)


class RequestEditView(PermissionRequiredMixin, UpdateView):
    permission_required = 'app_crm.change_requests'
    login_url = reverse_lazy('login')

    model = Requests
    form_class = EditRequestForm
    template_name = 'app_crm/create_or_edit_request.html'

    def get_success_url(self):
        return reverse('request_detail', args=[self.kwargs['pk']])


class RequestDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'app_crm.delete_requests'
    login_url = reverse_lazy('login')

    model = Requests
    template_name = 'app_crm/delete_request.html'
    success_url = reverse_lazy('requests_list')


class RequestsListView(PermissionRequiredMixin, ListFilteredView):
    permission_required = 'app_crm.view_requests_list'
    login_url = reverse_lazy('login')

    template_name = 'app_crm/requests_list.html'
    filter_set = RequestsFilter
    queryset = Requests.objects.all().order_by("-creation_date")
    context_object_name = 'requests_list'


class RequestDetailView(UserPassesTestMixin, DetailView):
    def test_func(self):
        return (
            self.request.user == self.get_object().customer or
            self.request.user.groups.filter(name='workers')
        )

    model = Requests
    template_name = 'app_crm/request_detail.html'
    context_object_name = 'request_detail'
