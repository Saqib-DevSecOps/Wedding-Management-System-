from src.website.models import Site , BackgroundImage

def get_site_information(request):
    site = Site.my_site()
    background = BackgroundImage.objects.all()
    background = background.order_by('created_on').first()
    context = {
        'name': site.name,
        'tagline': site.tagline,
        'description': site.description,
        'logo': site.logo.url if site.logo else "https://placehold.co/50",
        'favico': site.favico.url if site.favico else "https://placehold.co/25",
        'phone': site.phone,
        'email': site.email,
        'address': site.address,
        'background' : background
    }
    return context
