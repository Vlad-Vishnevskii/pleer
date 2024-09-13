
from typing import Set
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Video, VideoCreate, AudioCreate, Comments, FollowersCount, IpModel, Check, User, ReelsCreate, ImagesCreate, BwCreate, SlowingCreate, SpeedCreate, RenderCreate, RendCreate, SlideshowCreate, Slideshow, VideoshowCreate, Videoshow


class CustomUserAdmin(UserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]
        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
            }
        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form


class WalletUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username','condition')

class CheckAdmin(admin.ModelAdmin):
    list_display = ('check_info', 'status', 'money')
    
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'file','author')
    list_display_links = ('id', 'file','author')
    search_fields = ('id','file','author')
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'date_joined', 'is_verified')
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'date_joined', 'is_verified')
    
admin.site.register(Video, VideoAdmin)
admin.site.register(Check, CheckAdmin)
admin.site.register(User, UserAdmin)