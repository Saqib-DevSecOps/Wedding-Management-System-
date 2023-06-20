from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, View

from src.website.filters import BlogFilter, EventFilter
from src.website.models import (
    Slider, Blog, Gallery, BlogCategory, Service, Event, Site, ContactRequest,
    SitePartner, SiteTestimonial , AboutUsSection
)
from django.contrib import messages


# Create your views here.


class Home(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['slider'] = Slider.objects.all()
        context['images'] = Gallery.objects.all()[:8]
        context['services'] = Service.objects.all()[:6]
        events = Event.objects.all()
        site = Site.objects.all()
        context['site'] = site.order_by('-created_on').first()
        site = site.order_by('-created_on').first()
        print(site.about_title) 
        context['events'] = events.order_by('-created_at').first()
        context['blogs'] = Blog.objects.all()[:3]
        context['partners'] = SitePartner.objects.all()
        context['testimonials'] = SiteTestimonial.objects.all()

        return context


class BlogList(ListView):
    model = Blog

    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        category = self.request.GET.get('category')
        if category and self.request is not None:
            post = Blog.objects.filter(category__id=category)
        else:
            post = Blog.objects.all().order_by('-created_at')
        context['recent_blogs'] = Blog.objects.order_by('-created_at')[:5]
        context['popular_blogs'] = Blog.objects.order_by('-visits', '-read_time')[:5]
        filter_posts = BlogFilter(self.request.GET, queryset=post)
        pagination = Paginator(filter_posts.qs, 12)
        page_number = self.request.GET.get('page')
        page_obj = pagination.get_page(page_number)
        context['blog_category'] = BlogCategory.objects.all()
        context['blogs'] = page_obj
        context['filter_form'] = filter_posts
        context['category'] = category
        return context


class BlogDetail(DetailView):
    model = Blog
    template_name = 'website/blog_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BlogDetail, self).get_context_data(**kwargs)
        context['recent_blogs'] = Blog.objects.order_by('-created_at')[:5]
        context['blog_category'] = BlogCategory.objects.all()
        return context


class EventList(ListView):
    model = Event
    template_name = 'website/event_list.html'
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        category = self.request.GET.get('category')
        if category and self.request is not None:
            post = Event.objects.filter(category__id=category)
        else:
            post = Event.objects.all().order_by('-created_at')
        context['old_events'] = Event.objects.order_by('created_at')[:5]
        filter_event = EventFilter(self.request.GET, queryset=post)
        pagination = Paginator(filter_event.qs, 1)
        page_number = self.request.GET.get('page')
        page_obj = pagination.get_page(page_number)
        context['event_category'] = BlogCategory.objects.all()
        context['events'] = page_obj
        context['filter_form'] = filter_event
        context['category'] = category
        return context


class EventDetail(DetailView):
    model = Event
    template_name = 'website/event_detail.html'


class GalleryList(ListView):
    model = Gallery

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GalleryList, self).get_context_data(**kwargs)
        category = self.request.GET.get('category')
        sub_category = self.request.GET.get('subcategory')
        print(category)
        print(sub_category)
        gallery_images = Gallery.objects.all()
        if category is not None:
            if sub_category is not None:
                gallery_images = gallery_images.filter(Q(category_id=sub_category) | Q(category_id=category))
            else:
                gallery_images = Gallery.objects.filter(category_id=category)
        else:
            gallery_images = gallery_images
        context['gallery_images'] = gallery_images
        return context


class AboutUs(TemplateView):
    template_name = 'website/about_us.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AboutUs, self).get_context_data(**kwargs)
        about = AboutUsSection.objects.all()
        context['about'] = about.order_by("created_on").first()
        return context

        
class ContactUs(View):
    template_name = 'website/contact_us.html'

    def get(self, request):
        context = {}
        site = Site.my_site()
        context['email'] = site.email
        context['phone'] = site.phone
        context['address'] = site.address

        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        site = Site.my_site()

        context['email'] = site.email
        context['phone'] = site.phone
        context['address'] = site.address

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if not all([message, subject, phone, email, name]):
            messages.error(request, "Please fill all the fields to contact.")
        else:
            ContactRequest.objects.create(
                name=name, email=email, phone=phone, subject=subject, message=message
            )
            messages.success(request, "Your message request processed successfully")

        return render(request, self.template_name, context)


class Services(ListView):
    model = Service
    context_object_name = 'objects'
    template_name = 'website/services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = Site.my_site().service_content
        return context


class TermsView(TemplateView):
    template_name = 'website/terms-and-conditions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['terms'] = Site.my_site().terms_content
        return context


class PrivacyView(TemplateView):
    template_name = 'website/privacy-policy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['privacy'] = Site.my_site().privacy_content
        return context
