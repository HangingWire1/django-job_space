from django.contrib import admin

from job_posts.models import Category, JobPost

# Register your models here.
admin.site.register(Category)
admin.site.register(JobPost)