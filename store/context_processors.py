# Context processor: adds cart count and categories to every template
from .models import Category, Cart


def shop_context(request):
    """
    This function runs on every page load.
    It sends cart count and categories to all templates
    so the navbar can show them without repeating code.
    """
    context = {
        'nav_categories': Category.objects.all(),
        'cart_count': 0,
    }

    # Only count cart items for logged-in users
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            total = 0
            for item in cart.items.all():
                total = total + item.quantity
            context['cart_count'] = total
        except Cart.DoesNotExist:
            context['cart_count'] = 0

    return context
