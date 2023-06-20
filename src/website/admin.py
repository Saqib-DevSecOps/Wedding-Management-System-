from django.contrib import admin
from .models import (
    GalleryCategory,
    Gallery,
    Slider,
    ServiceCategory,
    Service,
    BlogCategory,
    Blog,
    EventCategory,
    Event,ServiceContent,Site,SitePartner,SiteTestimonial,ContactRequest,AboutUsSection , BackgroundImage

)


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('category', 'image', 'created_at', 'updated_at')
    list_filter = ('category',)


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('tag_1', 'tag_2', 'tag_3', 'image', 'created_at', 'updated_at')


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'image')
    list_filter = ('category',)


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'category', 'author')
    search_fields = ('title', 'author__username')


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'host', 'category', 'status', 'start_date', 'end_date', 'created_at', 'updated_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'host', 'category__name')

admin.site.register(ServiceContent)
admin.site.register(Site)
admin.site.register(SitePartner)
admin.site.register(SiteTestimonial)
admin.site.register(ContactRequest)
admin.site.register(AboutUsSection)
admin.site.register(BackgroundImage)
# Register your models here.
