from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from .models import Order, Product, Category
from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404
from .models import Cart, CartItem ,OrderItem

def home(request):
    # Pass products and categories to the home page template
    featured_products = Product.objects.all()[:4]
    best_sellers = Product.objects.all().order_by('-created_at')[:4]
    categories = Category.objects.all()

    return render(request, 'home.html', {
        'featured_products': featured_products,
        'best_sellers': best_sellers,
        'categories': categories,
    })


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('home')

    else:

        form = RegisterForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )


@login_required
def profile_view(request):

    return render(
        request,
        'profile.html'
    )


def logout_view(request):

    logout(request)

    return redirect('home')
def product_list(request):

    products = Product.objects.all()

    category_id = request.GET.get('category')

    search = request.GET.get('search')

    if category_id:

        products = products.filter(
            category_id=category_id
        )

    if search:

        products = products.filter(
            name__icontains=search
        )

    paginator = Paginator(
        products,
        6
    )

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(
        page_number
    )

    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'categories': categories,
    }

    return render(
        request,
        'products/product_list.html',
        context
    )
def product_detail(request, slug):

    product = Product.objects.get(
        slug=slug
    )

    # Related products from the same category
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    return render(
        request,
        'products/product_detail.html',
        {
            'product': product,
            'related_products': related_products,
        }
    )

@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    # Read quantity from form (default is 1)
    quantity = int(request.POST.get('quantity', 1))

    if not created:
        cart_item.quantity = cart_item.quantity + quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()

    return redirect('cart')

@login_required
def cart_view(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = cart.items.all()

    context = {
        'cart': cart,
        'items': items
    }

    return render(
        request,
        'cart/cart.html',
        context
    )

@login_required
def remove_from_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id
    )

    item.delete()

    return redirect('cart')

@login_required
def update_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id
    )

    quantity = request.POST.get(
        'quantity'
    )

    item.quantity = quantity

    item.save()

    return redirect('cart')

@login_required
def checkout(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = cart.items.all()

    if not items:
        return redirect('cart')

    if request.method == 'POST':

        order = Order.objects.create(
            user=request.user,
            total_amount=cart.get_total()
        )

        for item in items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        items.delete()

        return redirect(
            'order_success',
            order_id=order.id
        )

    return render(
        request,
        'orders/checkout.html',
        {
            'cart': cart,
            'items': items
        }
    )

@login_required
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    return render(
        request,
        'orders/order_success.html',
        {'order': order}
    )
@login_required
def order_history(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'orders/order_history.html',
        {'orders': orders}
    )


def page_not_found(request, exception):
    """Custom 404 error page"""
    return render(request, '404.html', status=404)