from django.urls import path
from .views import (
    DashboardView,
    UserListView, UserPasswordResetView, UserDetailView, UserUpdateView, GuestGroupListView, GuestGroupUpdateView,
    GuestGroupDetailView
)


app_name = 'admins'
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),

    path('guest/group/list/', GuestGroupListView.as_view(), name='guest-group-list'),
    path('guest-group/<int:pk>/detail/', GuestGroupDetailView.as_view(), name='guest-group-detail'),
    path('guest-group/<int:pk>/update/', GuestGroupUpdateView.as_view(), name='guest-group-update'),

    path('user/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('user/<int:pk>/change/', UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/password/reset/', UserPasswordResetView.as_view(), name='user-password-reset-view'),

]
