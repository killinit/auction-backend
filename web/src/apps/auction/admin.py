from django.contrib import admin

# Register your models here.
from .models import Category, Product, Review, Bid, ProductCategory


class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Category

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)


class ReviewAdmin(admin.ModelAdmin):
    class Meta:
        model = Review

admin.site.register(Review, ReviewAdmin)


class BidAdmin(admin.ModelAdmin):
    class Meta:
        model = Bid

admin.site.register(Bid, BidAdmin)


class ProductCategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = ProductCategory

admin.site.register(ProductCategory, ProductCategoryAdmin)
