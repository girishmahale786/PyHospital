from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

TYPE = (
    ('Default', '--- Select Designation ---'),
    ('Doctor', 'Doctor'),
    ('Patient', 'Patient'),
)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=255, choices=TYPE)
    address_line_1 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=255)
    profile_picture = models.ImageField()


class Appointment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Patient')
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Doctor')
    required_speciality = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='', editable=False,
                            unique=True, max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    draft = models.BooleanField()
    image = models.ImageField()
    date = models.DateField(auto_now=True)
    summary = models.TextField()
    content = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.slug == '':
            self.slug = f"{self.pk}-{slugify(self.title)}"
            self.save()

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug
        }
        return reverse('post-details', kwargs=kwargs)
