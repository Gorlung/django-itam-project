from django.contrib import admin
from assets_app.models import Category, Location, Vendor, State, Asset, Change, Employee
from mptt.admin import MPTTModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'Employee ITAM profile'
    filter_horizontal = ('permitted_locations',)
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)

# Register your models here.
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Location)
admin.site.register(Vendor)
admin.site.register(State)
admin.site.register(Asset)
admin.site.register(Change)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)