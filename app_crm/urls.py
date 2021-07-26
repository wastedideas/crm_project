from django.urls import path
from app_crm.views import (
    RequestCreateView,
    RequestEditView,
    RequestDeleteView,
    RequestsListView,
    RequestDetailView,
)
from django.views.generic import TemplateView

urlpatterns = [
    path(
        '',
        TemplateView.as_view(
            template_name='app_crm/main_page.html'
        ),
        name='main_page',
    ),
    path(
        'request/create/',
        RequestCreateView.as_view(),
        name='create_request',
    ),
    path(
        'request/<int:pk>/edit/',
        RequestEditView.as_view(),
        name='edit_request',
    ),
    path(
        'request/<int:pk>/delete/',
        RequestDeleteView.as_view(),
        name='delete_request',
    ),
    path(
        'requests/',
        RequestsListView.as_view(),
        name='requests_list',
    ),
    path(
        'request/<int:pk>/',
        RequestDetailView.as_view(),
        name='request_detail',
    ),
]
