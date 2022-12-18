from django.contrib import admin
from .models import Country
from .models import CountriesHistory
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

User = get_user_model()
admin.site.register(Country)
admin.site.register(CountriesHistory)

class SubscriptionInline(admin.TabularInline):
    model = Country.subscription.through
admin.site.unregister(User)
@admin.register(User) #admin.site.register(User,UserAdmin)
class UserAdmin(auth_admin.UserAdmin):
    inlines = [SubscriptionInline]

