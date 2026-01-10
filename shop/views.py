from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, Category, Cart, Order, OrderItem
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# ==================== HOME & PRODUCT VIEWS ====================

def home(request):
    """Home page with featured products"""
    featured_products = Product.objects.filter(featured=True, available=True)[:8]
    categories = Category.objects.all()[:6]
    latest_products = Product.objects.filter(available=True).order_by('-created')[:8]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'latest_products': latest_products,
    }
    return render(request, 'shop/home.html', context)


def product_list(request):
    """Product listing page with filters and search"""
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    
    # Filter by category
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Sorting
    sort_option = request.GET.get('sort')
    if sort_option == 'low':
        products = products.order_by('price')
    elif sort_option == 'high':
        products = products.order_by('-price')
    elif sort_option == 'new':
        products = products.order_by('-created')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    context = {
        'products': products_page,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category, 
        available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'shop/product_detail.html', context)


# ==================== CART VIEWS ====================

@login_required
def cart_view(request):
    """Display the shopping cart"""
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    cart_total = sum(item.get_total() for item in cart_items)
    item_count = cart_items.count()
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'item_count': item_count,
    }
    return render(request, 'shop/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """Add a product to cart or update quantity if already exists"""
    product = get_object_or_404(Product, id=product_id, available=True)
    
    # Check if product is in stock
    if product.stock < 1:
        messages.error(request, f'{product.name} is out of stock')
        return redirect('product_detail', slug=product.slug)
    
    # Get or create cart item for this user and product
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        # Item already in cart, increase quantity
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'Updated {product.name} quantity in cart')
        else:
            messages.warning(request, f'Cannot add more {product.name}. Only {product.stock} in stock.')
    else:
        messages.success(request, f'Added {product.name} to cart')
    
    return redirect('cart_view')


@login_required
def update_cart(request, item_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            # Check if requested quantity is available
            if quantity <= cart_item.product.stock:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Cart updated successfully')
            else:
                messages.error(request, f'Only {cart_item.product.stock} items available in stock')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart')
    
    return redirect('cart_view')


@login_required
def remove_from_cart(request, item_id):
    """Remove an item from the cart"""
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'Removed {product_name} from cart')
    return redirect('cart_view')


@login_required
def clear_cart(request):
    """Clear all items from the cart"""
    if request.method == 'POST':
        Cart.objects.filter(user=request.user).delete()
        messages.success(request, 'Cart cleared successfully')
    return redirect('cart_view')


# ==================== CHECKOUT & ORDER VIEWS ====================

@login_required
def checkout(request):
    """Checkout page"""
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty')
        return redirect('cart_view')
    
    cart_total = sum(item.get_total() for item in cart_items)
    
    if request.method == 'POST':
        # Process checkout - create order
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            postal_code=request.POST.get('postal_code'),
            country=request.POST.get('country'),
            total_amount=cart_total,
            status='pending'
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            
            # Reduce stock
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart_items.delete()
        
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('order_success', order_id=order.id)
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'shop/checkout.html', context)


# @login_required
# def my_orders(request):
#     """Display user's orders"""
#     orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    
#     context = {
#         'orders': orders,
#     }
#     return render(request, 'shop/my_orders.html', context)
@login_required
def my_orders(request):
    """Display user's orders"""
    # Get all orders for current user with their items
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    
    # Debug: Print to console
    print(f"User: {request.user}")
    print(f"Orders found: {orders.count()}")
    
    context = {
        'orders': orders,
    }
    return render(request, 'shop/my_orders.html', context)

@login_required
def order_success(request, order_id):
    """Order success page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'shop/order_success.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'shop/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'shop/register.html', {'form': form})

# def logout_view(request):
#     logout(request)
#     messages.success(request, 'Logged out successfully!')
#     return redirect('home')
def logout_view(request):
    """Logout the user"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')