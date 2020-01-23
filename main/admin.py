from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as CoreUserAdmin
from main.models import User, Target, Baz, SentBaz


class TargetInline(admin.TabularInline):
    model = Target


class UserAdmin(CoreUserAdmin):
    fieldsets = CoreUserAdmin.fieldsets + (
        (None, {'fields': ('interval',)}),
    )
    inlines = [TargetInline, ]


class SentBazInline(admin.TabularInline):
    model = SentBaz


class BazAdmin(admin.ModelAdmin):
    inlines = [SentBazInline, ]


class TargetAdmin(admin.ModelAdmin):
    inlines = [SentBazInline, ]


admin.site.register(User, UserAdmin)
admin.site.register(Target, TargetAdmin)
admin.site.register(Baz, BazAdmin)
admin.site.register(SentBaz)

