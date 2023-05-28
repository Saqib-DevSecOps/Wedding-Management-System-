from django.urls import path, include
from .views import (
    DashboardView,
    UserListView, UserPasswordResetView, UserDetailView, UserUpdateView, GuestGroupListView, GuestGroupUpdateView,
    GuestGroupDetailView, ProviderListCreateView, ProviderCreateView, ProviderUpdateView, ProviderDetailView,
    ProviderDeleteView
)

app_name = 'admins'
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),

    path('guest/group/list/', GuestGroupListView.as_view(), name='guest-group-list'),
    path('guest-group/<int:pk>/detail/', GuestGroupDetailView.as_view(), name='guest-group-detail'),
    path('guest-group/<int:pk>/update/', GuestGroupUpdateView.as_view(), name='guest-group-update'),
]
urlpatterns +=[

    path('provider/list/', ProviderListCreateView.as_view(), name='provider-list'),
    path('provider/create/', ProviderCreateView.as_view(), name='provider-create'),
    path('provider/detail/<str:pk>', ProviderDetailView.as_view(), name='provider-detail'),
    path('provider/update/<str:pk>', ProviderUpdateView.as_view(), name='provider-update'),
    path('provider/delete/<str:pk>', ProviderDeleteView.as_view(), name='provider-delete'),

    path('user/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('user/<int:pk>/change/', UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/password/reset/', UserPasswordResetView.as_view(), name='user-password-reset-view'),

]

urlpatterns += [
    path('json/', include('src.administration.admins.admins-json.urls', namespace='admins-json'))
]
