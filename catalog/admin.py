from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Автоматически заполняет slug на основе названия

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Позволяет добавлять картинки прямо на странице создания товара

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_active')  # название, цена, остаток, активность [cite: 54]
    list_filter = ('category', 'is_active')                 # фильтры сбоку [cite: 56]
    search_fields = ('name',)                               # поиск по названию [cite: 55]
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_main')