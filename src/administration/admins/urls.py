from django.urls import path, include
from .views import (
    DashboardView,
    GuestGroupListView, GuestGroupUpdateView,
    GuestGroupDetailView, ProviderListCreateView, ProviderCreateView, ProviderUpdateView, ProviderDetailView,
    ProviderDeleteView, GuestListView, GuestDeleteView, GuestGroupDeleteView, update_row_order, get_guests,
    InvitationUpdateView,
)

app_name = 'admins'
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),
]

urlpatterns += [

    path('guest/group/list/', GuestGroupListView.as_view(), name='guest-group-list'),
    path('guest-group/<int:pk>/detail/', GuestGroupDetailView.as_view(), name='guest-group-detail'),
    path('guest-group/<int:pk>/update/', GuestGroupUpdateView.as_view(), name='guest-group-update'),
    path('guest-group/<int:pk>/delete/', GuestGroupDeleteView.as_view(), name='guest-group-delete'),
    path('update_row_order/', update_row_order, name='update_row_order'),
    path('invitation/update/<str:pk>', InvitationUpdateView.as_view(), name='update-invitation'),
]
urlpatterns += [

    path('provider/list/', ProviderListCreateView.as_view(), name='provider-list'),
    path('provider/create/', ProviderCreateView.as_view(), name='provider-create'),
    path('provider/detail/<str:pk>', ProviderDetailView.as_view(), name='provider-detail'),
    path('provider/update/<str:pk>', ProviderUpdateView.as_view(), name='provider-update'),
    path('provider/delete/<str:pk>', ProviderDeleteView.as_view(), name='provider-delete'),

]


urlpatterns += [

    path('group/list/', GuestListView.as_view(), name='guest-list'),
    path('guest/<int:pk>/delete/', GuestDeleteView.as_view(), name='guest-delete'),
    path('get_guests/', get_guests, name='get_guests'),
]

urlpatterns += [
    path('json/', include('src.administration.admins.admins-json.urls', namespace='admins-json'))
]