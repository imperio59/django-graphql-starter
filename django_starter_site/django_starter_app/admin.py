from django.contrib import admin

from .models import Blip, Comment, UserProfile

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at']
    date_hierarchy = 'updated_at'
    search_fields = list(
        ['id', 'user__id', 'user__email'])


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Blip)
admin.site.register(Comment)
