from django.contrib import admin
from profiles_app.models import UserProfile, ProfileFeedItem


admin.site.register(UserProfile)
admin.site.register(ProfileFeedItem)