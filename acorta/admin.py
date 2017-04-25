from django.contrib import admin

# Register your models here.
from acorta.models import ShortedUrl

admin.site.register(ShortedUrl)
