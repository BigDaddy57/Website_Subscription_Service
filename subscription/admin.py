from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Subscription, Comment, User

class SubscriptionInline(admin.StackedInline):
    model = Subscription
    can_delete = False
    verbose_name_plural = 'subscription'

class UserAdmin(BaseUserAdmin):
    inlines = (SubscriptionInline,)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment_text', 'timestamp')

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Comment, CommentAdmin)
