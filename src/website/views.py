from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from src.website.filters import BlogFilter
from src.website.models import Slider, Blog, Gallery, BlogCategory


# Create your views here.


class Home(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['slider'] = Slider.objects.all()
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


class ContactUs(TemplateView):
    template_name = 'website/contact_us.html'
