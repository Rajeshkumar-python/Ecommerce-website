# # from django.db import models
# # from django.contrib.auth.models import User
# # from django.utils.text import slugify


# # # models.py
# # from django.db import models
# # from django.contrib.auth.models import User

# # class Category(models.Model):
# #     name = models.CharField(max_length=200)
# #     slug = models.SlugField(unique=True)
# #     created_at = models.DateTimeField(auto_now_add=True)

# #     class Meta:
# #         verbose_name_plural = 'Categories'

# #     def __str__(self):
# #         return self.name

# # class Product(models.Model):
# #     name = models.CharField(max_length=200)
# #     slug = models.SlugField(unique=True)
# #     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
# #     description = models.TextField()
# #     price = models.DecimalField(max_digits=10, decimal_places=2)
# #     original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
# #     image = models.ImageField(upload_to='products/')
# #     is_available = models.BooleanField(default=True)
# #     stock = models.IntegerField(default=0)
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     updated_at = models.DateTimeField(auto_now=True)

# #     def __str__(self):
# #         return self.name

# #     @property
# #     def discount_percentage(self):
# #         if self.original_price and self.original_price > self.price:
# #             return int(((self.original_price - self.price) / self.original_price) * 100)
# #         return 0

# # class Cart(models.Model):
# #     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
# #     session_key = models.CharField(max_length=40, null=True, blank=True)
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     updated_at = models.DateTimeField(auto_now=True)

# #     def __str__(self):
# #         return f"Cart {self.id}"

# #     @property
# #     def total_price(self):
# #         return sum(item.subtotal for item in self.items.all())

# #     @property
# #     def total_items(self):
# #         return sum(item.quantity for item in self.items.all())

# # class CartItem(models.Model):
# #     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
# #     product = models.ForeignKey(Product, on_delete=models.CASCADE)
# #     quantity = models.PositiveIntegerField(default=1)
# #     added_at = models.DateTimeField(auto_now_add=True)

# #     class Meta:
# #         unique_together = ('cart', 'product')

# #     def __str__(self):
# #         return f"{self.quantity} x {self.product.name}"

# #     @property
# #     def subtotal(self):
# #         return self.quantity * self.product.price

# # # from django.db import models
# # # from django.contrib.auth.models import User



# # # class Cart(models.Model):
# # #     user = models.ForeignKey(User, on_delete=models.CASCADE)
# # #     product = models.ForeignKey(Product, on_delete=models.CASCADE)
# # #     quantity = models.PositiveIntegerField(default=1)

# # #     def __str__(self):
# # #         return f"{self.product.name} - {self.quantity}"


# # class Cart(models.Model):
# #     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
# #     session_key = models.CharField(max_length=40, null=True, blank=True)
# #     created = models.DateTimeField(auto_now_add=True)
# #     updated = models.DateTimeField(auto_now=True)

# #     def __str__(self):
# #         return f"Cart {self.id}"


# #     def get_total(self):
# #         return sum(item.get_subtotal() for item in self.items.all())

# # class CartItem(models.Model):
# #     cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
# #     product = models.ForeignKey(Product, on_delete=models.CASCADE)
# #     quantity = models.PositiveIntegerField(default=1)
# #     added_at= models.DateTimeField(auto_now_add=True)

# #     def __str__(self):
# #         return f"{self.quantity} x {self.product.name}"

# #     def get_subtotal(self):
# #         return self.product.price * self.quantity

# # class Order(models.Model):
# #     STATUS_CHOICES = [
# #         ('pending', 'Pending'),
# #         ('processing', 'Processing'),
# #         ('shipped', 'Shipped'),
# #         ('delivered', 'Delivered'),
# #         ('cancelled', 'Cancelled'),
# #     ]
    
# #     user = models.ForeignKey(User, on_delete=models.CASCADE)
# #     full_name = models.CharField(max_length=200)
# #     email = models.EmailField()
# #     address = models.TextField()
# #     city = models.CharField(max_length=100)
# #     postal_code = models.CharField(max_length=20)
# #     country = models.CharField(max_length=100)
# #     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
# #     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     updated_at = models.DateTimeField(auto_now=True)
    
# #     def __str__(self):
# #         return f"Order {self.id} - {self.full_name}"


# # class OrderItem(models.Model):
# #     order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
# #     product = models.ForeignKey(Product, on_delete=models.CASCADE)
# #     quantity = models.PositiveIntegerField()
# #     price = models.DecimalField(max_digits=10, decimal_places=2)
    
# #     def __str__(self):
# #         return f"{self.quantity} x {self.product.name}"
    
# #     def get_total(self):
# #         return self.price * self.quantity
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from django.http import JsonResponse
# from django.views.decorators.http import require_POST
# from .models import Product, Category, Cart, CartItem

# def get_or_create_cart(request):
#     """Get or create cart for user or session"""
#     if request.user.is_authenticated:
#         cart, created = Cart.objects.get_or_create(user=request.user)
#     else:
#         if not request.session.session_key:
#             request.session.create()
#         session_key = request.session.session_key
#         cart, created = Cart.objects.get_or_create(session_key=session_key)
#     return cart

# def home(request):
#     """Home page view"""
#     return render(request, 'shop/home.html')
# from django.db import models
# from django.utils.text import slugify

# class Product(models.Model):
#     STOCK_STATUS_CHOICES = [
#         ('in_stock', 'In Stock'),
#         ('out_of_stock', 'Out of Stock'),
#         ('low_stock', 'Low Stock'),
#     ]
    
#     name = models.CharField(max_length=200)
#     slug = models.SlugField(max_length=200, unique=True, blank=True)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # THIS LINE
#     image = models.ImageField(upload_to='products/', blank=True, null=True)
#     category = models.CharField(max_length=100, blank=True)
#     stock = models.IntegerField(default=0)
#     stock_status = models.CharField(max_length=20, choices=STOCK_STATUS_CHOICES, default='in_stock')
#     available = models.BooleanField(default=True)
#     featured = models.BooleanField(default=False)
#     is_new = models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         ordering = ['-created']
    
#     def __str__(self):
#         return self.name
    
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.name)
#         super().save(*args, **kwargs) 
# @require_POST
# def add_to_cart(request, product_id):
#     """Add product to cart"""
#     product = get_object_or_404(Product, id=product_id, available=True)
#     cart = get_or_create_cart(request)
    
#     # Check stock
#     if product.stock <= 0:
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#             return JsonResponse({'success': False, 'message': 'Product out of stock'})
#         messages.error(request, 'Product is out of stock')
#         return redirect('product_list')
    
#     # Get or create cart item
#     cart_item, created = CartItem.objects.get_or_create(
#         cart=cart,
#         product=product,
#         defaults={'quantity': 1}
#     )
    
#     if not created:
#         if cart_item.quantity < product.stock:
#             cart_item.quantity += 1
#             cart_item.save()
#         else:
#             if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#                 return JsonResponse({'success': False, 'message': 'Not enough stock available'})
#             messages.warning(request, 'Not enough stock available')
#             return redirect('product_list')
    
#     # Calculate cart totals
#     cart_count = sum(item.quantity for item in cart.items.all())
#     cart_total = sum(item.quantity * item.product.price for item in cart.items.all())
    
#     # AJAX response
#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         return JsonResponse({
#             'success': True,
#             'message': 'Product added to cart',
#             'cart_count': cart_count,
#             'cart_total': str(cart_total)
#         })
    
#     messages.success(request, f'{product.name} added to cart')
#     return redirect('product_list')
# def cart_view(request):
#     # Get or create cart
#     if request.user.is_authenticated:
#         cart, created = Cart.objects.get_or_create(user=request.user)
#     else:
#         session_key = request.session.session_key
#         if not session_key:
#             request.session.create()
#             session_key = request.session.session_key
#         cart, created = Cart.objects.get_or_create(session_key=session_key)
    
#     cart_items = cart.items.all()
#     cart_total = cart.get_total()
    
#     context = {
#         'cart': cart,
#         'cart_items': cart_items,
#         'cart_total': cart_total,
#     }
#     return render(request, 'shop/cart.html', context)

# def update_cart_item(request):
#     if request.method == 'POST':
#         item_id = request.POST.get('item_id')
#         quantity = int(request.POST.get('quantity', 1))
        
#         try:
#             cart_item = CartItem.objects.get(id=item_id)
#             if quantity > 0:
#                 cart_item.quantity = quantity
#                 cart_item.save()
#             else:
#                 cart_item.delete()
            
#             cart_total = cart_item.cart.get_total()
#             item_subtotal = cart_item.get_subtotal() if quantity > 0 else 0
            
#             return JsonResponse({
#                 'success': True,
#                 'cart_total': float(cart_total),
#                 'item_subtotal': float(item_subtotal)
#             })
#         except CartItem.DoesNotExist:
#             return JsonResponse({'success': False, 'message': 'Item not found'})
    
#     return JsonResponse({'success': False, 'message': 'Invalid request'})

# def remove_cart_item(request):
#     if request.method == 'POST':
#         item_id = request.POST.get('item_id')
        
#         try:
#             cart_item = CartItem.objects.get(id=item_id)
#             cart = cart_item.cart
#             cart_item.delete()
            
#             cart_total = cart.get_total()
#             cart_count = sum(item.quantity for item in cart.items.all())
            
#             return JsonResponse({
#                 'success': True,
#                 'cart_total': float(cart_total),
#                 'cart_count': cart_count
#             })
#         except CartItem.DoesNotExist:
#             return JsonResponse({'success': False, 'message': 'Item not found'})
    
#     return JsonResponse({'success': False, 'message': 'Invalid request'})
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    STOCK_CHOICES = [
        ('in_stock', 'In Stock'),
        ('low_stock', 'Low Stock'),
        ('out_stock', 'Out of Stock'),
    ]
    
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.IntegerField(default=0)
    stock_status = models.CharField(max_length=20, choices=STOCK_CHOICES, default='in_stock')
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    discount_percent = models.IntegerField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    review_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     session_key = models.CharField(max_length=255, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.product.name} - {self.quantity}"


# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
    
#     def __str__(self):
#         return f"{self.quantity} x {self.product.name}"
    
#     def get_total(self):
#         return self.product.price * self.quantity
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensure one user can't have duplicate products in cart
        unique_together = ('user', 'product')
        ordering = ['-created']

    def __str__(self):
        return f'{self.user.username} - {self.product.name} ({self.quantity})'

    def get_total(self):
        """Calculate total price for this cart item"""
        return self.product.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_total(self):
        return self.price * self.quantity
    
  