from django.contrib import admin
from .models import Property, PropertyFeature, Image

# customizing the admin interface title and everything
admin.site.site_header = 'house admin'
admin.site.site_title = 'admin panel'
admin.site.index_title = 'welcome to the house admin home'

class ImageInline(admin.TabularInline):
    model = Image
    extra = 3

class PropertyAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ('title', 'city', 'price', 'address', 'listed_at', 'status')
    list_filter = ('status', 'city', 'price')
    search_fields = ('name', 'city', 'address')
    # prepopulated_fields = {'slug': ('name', 'city')}
    ordering = ('-updated_at',)
 
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('price', 'payment_mode', 'description', 'added_at')
    list_filter = ('payment_mode', 'price', 'added_at')
    search_fields = ('amount', 'order__status', 'added_at')
    ordering = ('-added_at',)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('payment', 'transaction_desc',  'transaction_type')
    list_filter = ( 'date_paid', 'transaction_type')
    search_fields = ( 'date_paid', 'transaction_type') 
    ordering = ('-date_paid',)

class PropertyFeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name', 'feature_value')
    list_filter = ('feature_name', 'feature_value')
    search_fields = ('feature_name', 'feature_value')
    ordering = ('-feature_name',)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_alt',)

admin.site.register(Property, PropertyAdmin )
admin.site.register(PropertyFeature, PropertyFeatureAdmin)
admin.site.register(Image, ImageAdmin)
