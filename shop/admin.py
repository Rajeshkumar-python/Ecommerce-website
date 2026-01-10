# from django.contrib import admin
# from .models import Category, Product, Cart, Order, OrderItem

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug']
#     prepopulated_fields = {'slug': ('name',)}

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug', 'price', 'stock', 'available']
#     list_filter = ['available', 'category']
#     list_editable = ['price', 'stock', 'available']
#     prepopulated_fields = {'slug': ('name',)}

# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     # Only include fields that exist in your Cart model
#     list_display = ['id','user', 'created_at','product']
#     # list_filter = ['user']
#     # search_fields = ['user__username', 'product__name']
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ('id','cart', 'product', 'quantity')

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     # Only include fields that exist in your Order model
#     list_display = ['id', 'user', 'total_amount', 'status']
#     list_filter = ['status']
#     search_fields = ['user__username', 'id']

# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ['order', 'product', 'quantity', 'price']
#     list_filter = ['order']
#     search_fields = ['product__name']


# from django.contrib import admin
# from .models import Category, Product, Cart, CartItem, Order, OrderItem

# # -------------------------
# # Category Admin
# # -------------------------
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug']
#     prepopulated_fields = {'slug': ('name',)}


# # -------------------------
# # Product Admin
# # -------------------------
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug', 'price', 'stock', 'available']
#     list_filter = ['available', 'category']
#     list_editable = ['price', 'stock', 'available']
#     prepopulated_fields = {'slug': ('name',)}


# # -------------------------
# # Cart Admin  (NO product here)
# # -------------------------
# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'created_at']
#     list_filter = ['user']
#     search_fields = ['user__username']


# # -------------------------
# # CartItem Admin (product & quantity belong here)
# # -------------------------
# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ['id', 'cart', 'product', 'quantity']
#     list_filter = ['cart']
#     search_fields = ['product__name']


# # -------------------------
# # Order Admin
# # -------------------------
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'total_amount', 'status']
#     list_filter = ['status']
#     search_fields = ['user__username', 'id']


# # -------------------------
# # OrderItem Admin
# # -------------------------
# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ['order', 'product', 'quantity', 'price']
#     list_filter = ['order']
#     search_fields = ['product__name']


from django.contrib import admin
from .models import Category, Product, Cart, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'stock_status', 'available', 'featured', 'created']
    list_filter = ['available', 'featured', 'category', 'stock_status', 'created']
    list_editable = ['price', 'stock', 'stock_status', 'available', 'featured']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    date_hierarchy = 'created'
    ordering = ['-created']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'get_total_display', 'created', 'updated']
    list_filter = ['created', 'updated']
    search_fields = ['user__username', 'product__name']
    readonly_fields = ['created', 'updated']
    date_hierarchy = 'created'
    
    def get_total_display(self, obj):
        return f'${obj.get_total():.2f}'
    get_total_display.short_description = 'Total'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'email', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['full_name', 'email', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'full_name', 'email')
        }),
        ('Shipping Information', {
            'fields': ('address', 'city', 'postal_code', 'country')
        }),
        ('Order Details', {
            'fields': ('total_amount', 'status', 'created_at', 'updated_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'get_total']
    list_filter = ['order__status']
    search_fields = ['product__name', 'order__id']
    raw_id_fields = ['order', 'product']