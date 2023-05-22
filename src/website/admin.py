from django.contrib import admin
from .models import BlogCategory,Blog,Slider,Gallery,ServiceCategory,GalleryCategory,Service,Event,EventCategory
# Register your models here.


admin.site.register(Slider)
admin.site.register(ServiceCategory)
admin.site.register(GalleryCategory)
admin.site.register(Gallery)
admin.site.register(Service)
admin.site.register(BlogCategory)
admin.site.register(Blog)
admin.site.register(Event)
admin.site.register(EventCategory)
