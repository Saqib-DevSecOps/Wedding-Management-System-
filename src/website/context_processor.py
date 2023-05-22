from src.website.models import GalleryCategory, EventCategory, ServiceCategory


def category(request):
    gallery = GalleryCategory.objects.filter(parent__isnull=True)
    services = ServiceCategory.objects.all()
    events = EventCategory.objects.all()
    return {
        'gallery': gallery,
        'services': services,
        'events': events,
    }
