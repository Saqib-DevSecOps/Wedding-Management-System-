from django.urls import path

from src.website.views import (
    Home, BlogList, GalleryList, AboutUs, ContactUs, Services, EventList, BlogDetail, EventDetail,
    TermsView, PrivacyView
)

app_name = "website"
urlpatterns = [
    path('', Home.as_view(), name='home'),

    path('blogs/', BlogList.as_view(), name='blog'),
    path('blog/<str:pk>/', BlogDetail.as_view(), name='blog_detail'),

    path('gallery/', GalleryList.as_view(), name='gallery'),
    path('services/', Services.as_view(), name='services'),

    path('events/', EventList.as_view(), name='events'),
    path('event/detail/<str:pk>', EventDetail.as_view(), name='event_detail'),

    path('about-us/', AboutUs.as_view(), name='about'),
    path('contact-us/', ContactUs.as_view(), name='contact-us'),

    path('terms-and-conditions/', TermsView.as_view(), name='terms-and-conditions'),
    path('privacy-policy/', PrivacyView.as_view(), name='privacy-policy'),
]
