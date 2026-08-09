from django.contrib import admin
from .models import Favorite, Image, Inquiry, Property, PropertyFeature, PropertyOffer

# customizing the admin interface title and everything
admin.site.site_header = 'house admin'
admin.site.site_title = 'admin panel'
admin.site.index_title = 'welcome to the house admin home'

class ImageInline(admin.TabularInline):
    model = Image
    extra = 3

class PropertyAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ('title', 'city', 'price', 'address', 'listed_at', 'status', 'moderation_status', 'created_by')
    list_filter = ('status', 'moderation_status', 'listing_type', 'property_type', 'city')
    search_fields = ('title', 'city', 'address', 'created_by__email')
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


class InquiryAdmin(admin.ModelAdmin):
    list_display = ('property', 'seeker', 'inquiry_type', 'status', 'created_at', 'updated_at')
    list_filter = ('inquiry_type', 'status')
    search_fields = ('property__title', 'seeker__email', 'message')
    readonly_fields = ('created_at', 'updated_at')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('property', 'user', 'created_at')
    search_fields = ('property__title', 'user__email')
    readonly_fields = ('created_at',)


class PropertyOfferAdmin(admin.ModelAdmin):
    list_display = ('property', 'seeker', 'provider', 'offer_type', 'amount', 'currency', 'status', 'expires_at')
    list_filter = ('offer_type', 'status', 'currency')
    search_fields = ('property__title', 'seeker__email', 'provider__email')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Property, PropertyAdmin )
admin.site.register(PropertyFeature, PropertyFeatureAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Inquiry, InquiryAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(PropertyOffer, PropertyOfferAdmin)
