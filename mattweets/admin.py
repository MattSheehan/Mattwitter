'''
COPYRIGHT Matt Sheehan 2021
'''
from django.contrib import admin
# Register models
from .models import Tweet


class AdminTweet(admin.ModelAdmin):
    list_display = ['__str__', 'user']
    search_fields = ['user__username__iexact', 'user__email']

    class Meta:
        model = Tweet


admin.site.register(Tweet, AdminTweet)
