from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from tinymce.models import HTMLField

from src.accounts.models import User


class GalleryCategory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Gallery Categories'


class Gallery(models.Model):
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category.name


class Slider(models.Model):
    tag_1 = models.CharField(max_length=30, null=True, blank=True)
    tag_2 = models.CharField(max_length=30, null=True, blank=True)
    tag_3 = models.CharField(max_length=30, null=True, blank=True)
    image = models.ImageField(upload_to='slider')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Sliders'


class ServiceCategory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Services Categories'


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='services/')
    description = models.TextField()

    def __str__(self):
        return self.name


class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Blog Categories'

    def __str__(self):
        return self.name


class Blog(models.Model):
    STATUS = (
        ('draft', "Draft"),
        ('publish', "Publish")
    )

    title = models.CharField(max_length=255, unique=True)
    thumbnail_image = models.ImageField(upload_to='books/images/posts', null=True, blank=True)
    slug = models.SlugField(unique=True, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, blank=False, null=True,
                                 related_name='blog_category')
    content = HTMLField()

    read_time = models.PositiveIntegerField(default=0, help_text='read time in minutes')
    visits = models.PositiveIntegerField(default=0)

    status = models.CharField(max_length=15, choices=STATUS, default='publish')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class EventCategory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Event Categories'

    def __str__(self):
        return self.name


class Event(models.Model):
    STATUS = (
        ('draft', "Draft"),
        ('publish', "Publish")
    )

    title = models.CharField(max_length=255)
    host = models.CharField(max_length=255, verbose_name="host name")
    thumbnail_image = models.ImageField(upload_to='books/images/posts')
    slug = models.SlugField(unique=True, null=False)
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, blank=False, null=True,
                                 related_name='event_category')
    content = HTMLField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    country = models.CharField(max_length=122)
    city = models.CharField(max_length=100)
    exact_destination = models.CharField(max_length=100)
    status = models.CharField(max_length=15, choices=STATUS, default='publish')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class ServiceContent(models.Model):
    content = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20]


class Site(models.Model):
    name = models.CharField(default='_ no name _', max_length=255)
    tagline = models.CharField(default="_ no tagline _", max_length=255)
    description = models.CharField(default="_ no description _", max_length=255)
    logo = models.ImageField(upload_to='site/logo', null=True, blank=True)
    dashboard_logo = models.ImageField(upload_to='site/logo', null=True, blank=True)
    favico = models.ImageField(upload_to='site/favico', null=True, blank=True)

    # ABOUT 
    about_title = models.CharField(max_length=200)
    about_short_discription = HTMLField(null=True, blank=True)
    about_image_1 = models.ImageField(upload_to='home/', null=True, blank=True)
    about_image_2 = models.ImageField(upload_to='home/', null=True, blank=True)
    about_image_3 = models.ImageField(upload_to='home/', null=True, blank=True)

    # Titles
    service_title = models.CharField(max_length=200, null=True, blank=True)
    event_title = models.CharField(max_length=200, null=True, blank=True)
    gallery_title = models.CharField(max_length=200, null=True, blank=True)
    blog_title = models.CharField(max_length=200, null=True, blank=True)

    # CONTACT
    address = models.CharField(max_length=1000, default='_ no address provided _')
    phone = models.CharField(max_length=15, default='+000000000000')
    email = models.EmailField(max_length=255, default='noname@domain.com')

    # PAGES
    privacy_content = HTMLField(default='*')
    terms_content = HTMLField(default='*')
    disclaimer_content = HTMLField(default='*')
    contact_content = HTMLField(default='*')
    service_content = HTMLField(default='*')

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Site"

    def __str__(self):
        return self.name

    @classmethod
    def my_site(cls):
        sites = Site.objects.all()
        if sites:
            return sites.first()
        return Site.objects.create()


class SitePartner(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    logo = models.ImageField(upload_to='site/partner/logo', null=True, blank=True)

    def __str__(self):
        return self.name


class SiteTestimonial(models.Model):
    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    image = models.ImageField(upload_to='site/partner/logo')

    def __str__(self):
        return self.name


class ContactRequest(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AboutUsSection(models.Model):
    image_1 = models.ImageField(upload_to="about/", null=True, blank=True)
    image_2 = models.ImageField(upload_to="about/", null=True, blank=True)
    image_3 = models.ImageField(upload_to="about/", null=True, blank=True)
    short_description = HTMLField(null=True, blank=True)
    description = HTMLField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"About Us {self.pk}"


class BackgroundImage(models.Model):
    event_background = models.ImageField(upload_to="background/", null=True, blank=True)
    service_background = models.ImageField(upload_to="background/", null=True, blank=True)
    gallery_background = models.ImageField(upload_to="background/", null=True, blank=True)
    blog_background = models.ImageField(upload_to="background/", null=True, blank=True)
    about_background = models.ImageField(upload_to="background/", null=True, blank=True)
    contact_background = models.ImageField(upload_to="background/", null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)
