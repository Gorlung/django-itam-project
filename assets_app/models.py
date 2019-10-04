from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone
from django.urls import reverse

class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    selectable_choices = (('Yes','Yes'),('No','No'))
    selectable = models.CharField(max_length=3, choices=selectable_choices, default='No')
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['name']
    def __str__(self):
        return self.name

class Location(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    selectable_choices = (('Yes','Yes'),('No','No'))
    selectable = models.CharField(max_length=3, choices=selectable_choices, default='No')
    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['name']
    def __str__(self):
        return self.name

class Vendor(models.Model):
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'
    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=20, unique=True)
    class Meta:
        verbose_name = 'State'
        verbose_name_plural = 'State'
    def __str__(self):
        return self.name

class Asset(models.Model):
    inventory_number = models.CharField(max_length=50, unique=True)
    model_name = models.CharField(max_length=50, unique=False, blank=False)
    category = TreeForeignKey('Category', on_delete=models.SET('UNCATEGORISED'), blank=False)
    location = TreeForeignKey('Location', on_delete=models.SET('NOT SET'), blank=False, null=True)
    serial_number = models.CharField(max_length=50, blank=False, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET('NOT SET'), blank=False, null=True)
    state = models.ForeignKey(State, on_delete=models.SET('NOT SET'), blank=False, null=True)
    aquisition_date = models.DateField(null=True)
    warranty_expiry_date = models.DateField(blank=True, null=True)
    added_on = models.DateTimeField(editable=False, default=timezone.now())
    modified_on = models.DateTimeField(editable=False, default=timezone.now())
    legal_entity = models.CharField(max_length=100, blank=True)
    invoice_number = models.CharField(max_length=50, blank=True)
    host_name = models.CharField(max_length=100, blank=True)
    comments = models.TextField(blank=True)
    def change(self):
        self.modified_on = timezone.now()
        self.save()
    def get_absolute_url(self):
        return reverse('asset_detail', kwargs={'pk': self.pk})
    
    class Meta:
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'
    def __str__(self):
        return self.inventory_number 

class Change(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, editable=False, related_name='assets')
    changed_on = models.DateTimeField(editable=False, default=timezone.now())
    change_details = models.TextField(editable=False)
    author = models.ForeignKey('auth.User', on_delete=models.SET('USER DELETED'), editable=False, null=True)
    class Meta:
        verbose_name = 'Change'
        verbose_name_plural = 'Changes'
    def __str__(self):
        return self.asset + ': ' + self.change_details
