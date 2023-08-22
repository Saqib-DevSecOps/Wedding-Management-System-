from django.urls import path, include
from django.views.generic import TemplateView

from .views import (
    DashboardView,
    GuestGroupListView,
    GuestGroupDetailView, ProviderListCreateView, ProviderCreateView, ProviderUpdateView, ProviderDetailView,
    ProviderDeleteView, GuestGroupDeleteView, update_row_order, get_guests,
    InvitationUpdateView, update_guest_group, SeatPlannerListView, SeatPlannerCreateView, CreateSeatPlannerViewApi,
    UpdateSeatPlanner, SeatPlannerDetail, SeatPlannerDelete, update_invitation_order, DownloadAttachmentView,
    save_guest_group, ExportGroupsToExcel, EventTimeLineCreateView, EventTimeLineDeleteView, EventTimeLineUpdateView,
    EventTimelineView, Test
)

app_name = 'admins'

urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),
]

urlpatterns += [

    path('guest/group/list/', GuestGroupListView.as_view(), name='guest-group-list'),
    path('guest/group/create/', save_guest_group, name='guest-group-create'),
    path('guest-group/<int:pk>/detail/', GuestGroupDetailView.as_view(), name='guest-group-detail'),
    path('update_guest_group/', update_guest_group, name='update_guest_group'),
    path('guest-group/<int:pk>/delete/', GuestGroupDeleteView.as_view(), name='guest-group-delete'),
    path('update_row_order/', update_row_order, name='update_row_order'),
    path('update_invitation_order/', update_invitation_order, name='update_invitation_order'),
    path('get_guests/', get_guests, name='get_guests'),
    path('invitation/update/<str:pk>/', InvitationUpdateView.as_view(), name='update-invitation'),
    path('export/', ExportGroupsToExcel.as_view(), name='export-groups-to-excel'),
]

urlpatterns += [

    path('provider/list/', ProviderListCreateView.as_view(), name='provider-list'),
    path('provider/create/', ProviderCreateView.as_view(), name='provider-create'),
    path('provider/detail/<str:pk>', ProviderDetailView.as_view(), name='provider-detail'),
    path('provider/update/<str:pk>', ProviderUpdateView.as_view(), name='provider-update'),
    path('provider/delete/<str:pk>', ProviderDeleteView.as_view(), name='provider-delete'),
    path('download/<str:provider_id>/', DownloadAttachmentView.as_view(), name='download-attachment'),

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

    path('event/timeline/', EventTimelineView.as_view(), name='event-timeline'),
    path('event/create/', EventTimeLineCreateView.as_view(), name='event-create'),
    path('event/delete/<str:pk>/', EventTimeLineDeleteView.as_view(), name='event-delete'),
    path('event/update/<str:pk>/', EventTimeLineUpdateView.as_view(), name='event-update'),

]

urlpatterns += [
    path('test/',Test.as_view(),name='test')
]

urlpatterns += [
    path('json/', include('src.administration.admins.admins-json.urls', namespace='admins-json'))
]
