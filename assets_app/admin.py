from django.contrib import admin
from assets_app.models import Category, Location, Vendor, State, Asset, Change
from mptt.admin import MPTTModelAdmin

# Register your models here.
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Location, MPTTModelAdmin)
admin.site.register(Vendor)
admin.site.register(State)
admin.site.register(Asset)
admin.site.register(Change)