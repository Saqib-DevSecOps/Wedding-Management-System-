from django.urls import path, include
from .views import (
    DashboardView,
    GuestGroupListView, GuestGroupUpdateView,
    GuestGroupDetailView, ProviderListCreateView, ProviderCreateView, ProviderUpdateView, ProviderDetailView,
    ProviderDeleteView, GuestGroupDeleteView, update_row_order, get_guests,
    InvitationUpdateView, update_guest_group, SeatPlannerListView, SeatPlannerCreateView, CreateSeatPlannerViewApi,
    UpdateSeatPlanner, SeatPlannerDetail, SeatPlannerDelete
)

app_name = 'admins'

urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),
]

urlpatterns += [

    path('guest/group/list/', GuestGroupListView.as_view(), name='guest-group-list'),
    path('guest-group/<int:pk>/detail/', GuestGroupDetailView.as_view(), name='guest-group-detail'),
    path('update_guest_group/', update_guest_group, name='update_guest_group'),
    path('guest-group/<int:pk>/delete/', GuestGroupDeleteView.as_view(), name='guest-group-delete'),
    path('update_row_order/', update_row_order, name='update_row_order'),
    path('get_guests/', get_guests, name='get_guests'),
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

    path('seat-planner/list/', SeatPlannerListView.as_view(), name='seat-planner-list'),
    path('seat-planner/create/', SeatPlannerCreateView.as_view(), name='seat-planner-create'),
    path('seat-planner/create/api/', CreateSeatPlannerViewApi.as_view(), name='seat-planner-create-api'),
    path('seat-planner/detail/<str:pk>/', SeatPlannerDetail.as_view(), name='seat-planner-detail'),
    path('seat-planner/delete/<str:pk>/', SeatPlannerDelete.as_view(), name='seat-planner-delete'),
    path('seat-planner/<str:pk>/update/', UpdateSeatPlanner.as_view(), name='seat-planner-update'),

]

urlpatterns += [
    path('json/', include('src.administration.admins.admins-json.urls', namespace='admins-json'))
]
