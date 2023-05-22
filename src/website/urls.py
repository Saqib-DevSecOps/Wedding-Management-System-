from django.urls import path

from src.website.models import Gallery
from src.website.views import Home, BlogList, GalleryList, AboutUs, ContactUs

app_name = "website"
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('blogs/', BlogList.as_view(), name='blog'),
    path('gallery/', GalleryList.as_view(), name='gallery'),
    path('about-us/', AboutUs.as_view(), name='about'),
    path('contact-us/', ContactUs.as_view(), name='contact-us'),
]
