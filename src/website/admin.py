from django.contrib import admin
from .models import BlogCategory,Blog,Slider,Gallery
# Register your models here.


admin.site.register(Slider)
admin.site.register(Gallery)
admin.site.register(BlogCategory)
admin.site.register(Blog)
