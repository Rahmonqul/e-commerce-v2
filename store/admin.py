from django.contrib import admin
from  .models import *
from django.utils.timezone import localtime
# Register your models here.
from mptt.admin import MPTTModelAdmin


class BrandInline(admin.TabularInline):
    model=Brand

class MediaInline(admin.TabularInline):
    model=Media

class VariantInline(admin.TabularInline):
    model=Variant

class VariantItemInline(admin.TabularInline):
    model=VariantItem

# class SubCategoryInline(admin.TabularInline):
#     model=SubCategory
#     prepopulated_fields = {'slug': ('title',)}

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    fields = ['user', 'answer_text', 'date_answered']
    readonly_fields = ['date_answered']

# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display = ['title', 'image']
#     list_editable = ['image']
#     prepopulated_fields = {'slug': ('title',)}
#     search_fields = ['title']

class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'image']

class CategoryAdmin(MPTTModelAdmin):
    list_display = ['title','parent' ,'image']
    list_editable = ['image']
    search_fields = ['title']
    # inlines = [SubCategoryInline]
    prepopulated_fields = {'slug':('title',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'regular_price', 'stock', 'featured', 'vendor', 'brand', 'date']
    search_fields = ['name', 'category__title']
    list_filter = [ 'status','featured']
    inlines = [MediaInline, VariantInline]
    prepopulated_fields = {'slug': ('name',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subcategory":
            category_id = request.POST.get('category')
            if category_id:
                kwargs['queryset'] = SubCategory.objects.filter(category_id=category_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class VariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'name']
    search_fields = ['product__name', 'name']
    inlines = [VariantItemInline]

class VarianItemAdmin(admin.ModelAdmin):
    list_display = ['variant', 'title', 'content']
    search_fields = ['variant__name', 'title']

class MediaAdmin(admin.ModelAdmin):
    list_display = ['product', 'media_id']
    search_fields = ['product__name', 'media_id']

class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'qty', 'price', 'subtotal_price', 'date']
    search_fields = ['id', 'product__name', 'user__username']
    list_filter = ['date', 'product']

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'vendor', 'discount']
    search_fields = ['code', 'vendor__username']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer', 'total', 'payment_status', 'order_status', 'payment_method', 'date']
    list_editable = ['payment_status', 'order_status', 'payment_method']
    search_fields = ['order_id', 'customer__username']
    list_filter = ['payment_status', 'order_status']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item_id', 'order', 'product', 'qty', 'price', 'initial_total']
    search_fields = ['item_id', 'order__order_id', 'product_name']
    list_filter = ['order__date']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'active', 'date']
    search_fields = ['user__username', 'product__name']
    list_filter = ['active', 'rating']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'question_text', 'active', 'date_asked', 'get_last_answer_date']
    search_fields = ['question_text', 'product__name']
    list_filter = ['active', 'date_asked']
    inlines = [AnswerInline]

    def get_last_answer_date(self, obj):
        last_answer = obj.answers.order_by('-date_answered').first()
        if last_answer:
            return localtime(last_answer.date_answered).strftime('%Y-%m-%d %H:%M:%S')
        return None
    get_last_answer_date.short_description = 'Date Answered'

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'user', 'answer_text', 'date_answered']
    search_fields = ['answer_text', 'question__product__name']
    list_filter = ['date_answered']

class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']
    list_filter = ['title']

class ServiseAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon','subtitle']
    list_filter = ['title']

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['code','name']

class VideosAdmin(admin.ModelAdmin):
    list_display = ['title']

# class ColorAdmin(admin.ModelAdmin):
#     list_display = ['name']
#
# class SizeAdmin(admin.ModelAdmin):
#     list_display = ['name']
#
# class StyleAdmin(admin.ModelAdmin):
#     list_display = ['name']

# class AdditionalInfoAdmin(admin.ModelAdmin):
#     list_display = ['text']

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Banners, BannerAdmin)
admin.site.register(Service, ServiseAdmin)
# admin.site.register(SubCategory, SuCategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(VariantItem, VarianItemAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Videos, VideosAdmin)
# admin.site.register(Color, ColorAdmin)
# admin.site.register(Size, SizeAdmin)
# admin.site.register(Style, StyleAdmin)
# admin.site.register(AdditionalInfo, AdditionalInfoAdmin)
