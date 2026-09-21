from decimal import Decimal
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Category, Order, OrderItem, DeliveryZone

def _cart(request):
    return request.session.get("cart", {})

def _save_cart(request, cart):
    request.session["cart"] = cart
    request.session.modified = True

def home(request):
    products = Product.objects.filter(active=True).select_related("category")
    q = request.GET.get("q", "").strip()
    cat = request.GET.get("cat", "").strip()
    if q:
        products = products.filter(name__icontains=q)
    if cat:
        products = products.filter(category__slug=cat)
    return render(request, "shop/home.html", {
        "products": products, "categories": Category.objects.all(), "q": q
    })

def product_detail(request, pk):
    return render(request, "shop/product.html", {
        "product": get_object_or_404(Product, pk=pk, active=True)
    })

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk, active=True)
    qty = max(1, int(request.POST.get("quantity", 1)))
    cart = _cart(request)
    key = str(pk)
    cart[key] = min(int(cart.get(key, 0)) + qty, product.stock)
    _save_cart(request, cart)
    messages.success(request, "Produit ajouté au panier.")
    return redirect("cart")

def cart(request):
    cart_data = _cart(request)
    items, subtotal = [], Decimal("0")
    for pk, qty in cart_data.items():
        product = get_object_or_404(Product, pk=int(pk), active=True)
        qty = min(int(qty), product.stock)
        if qty <= 0:
            continue
        total = product.price * qty
        subtotal += total
        items.append({"product": product, "quantity": qty, "total": total})
    return render(request, "shop/cart.html", {"items": items, "subtotal": subtotal})

def update_cart(request, pk):
    cart = _cart(request)
    qty = max(0, int(request.POST.get("quantity", 0)))
    product = get_object_or_404(Product, pk=pk, active=True)
    if qty == 0:
        cart.pop(str(pk), None)
    else:
        cart[str(pk)] = min(qty, product.stock)
    _save_cart(request, cart)
    return redirect("cart")

def remove_from_cart(request, pk):
    cart = _cart(request)
    cart.pop(str(pk), None)
    _save_cart(request, cart)
    return redirect("cart")

def checkout(request):
    cart_data = _cart(request)
    if not cart_data:
        messages.info(request, "Votre panier est vide.")
        return redirect("home")
    products, subtotal = [], Decimal("0")
    for pk, qty in cart_data.items():
        product = get_object_or_404(Product, pk=int(pk), active=True)
        qty = min(int(qty), product.stock)
        products.append((product, qty))
        subtotal += product.price * qty
    zones = DeliveryZone.objects.filter(active=True)
    if request.method == "POST":
        zone = get_object_or_404(DeliveryZone, pk=request.POST.get("zone"))
        order = Order.objects.create(
            customer_name=request.POST["customer_name"],
            phone=request.POST["phone"],
            email=request.POST.get("email", ""),
            address=request.POST["address"],
            city=request.POST.get("city", "Lomé"),
            zone=zone,
            notes=request.POST.get("notes", ""),
            payment_method=request.POST.get("payment_method", "cash"),
            delivery_fee=zone.fee,
        )
        for product, qty in products:
            if qty <= 0:
                continue
            OrderItem.objects.create(order=order, product=product, quantity=qty, unit_price=product.price)
            product.stock = max(0, product.stock - qty)
            product.save(update_fields=["stock"])
        request.session["cart"] = {}
        messages.success(request, f"Commande #{order.id} enregistrée.")
        return redirect("order_detail", pk=order.id)
    return render(request, "shop/checkout.html", {
        "products": products, "subtotal": subtotal, "zones": zones
    })

def order_detail(request, pk):
    return render(request, "shop/order.html", {"order": get_object_or_404(Order, pk=pk)})

def dashboard(request):
    orders = Order.objects.all()
    revenue = sum(o.grand_total() for o in orders.exclude(status="cancelled"))
    low = Product.objects.filter(active=True, stock__lte=10).order_by("stock")
    return render(request, "shop/dashboard.html", {
        "orders_count": orders.count(),
        "pending": orders.filter(status="pending").count(),
        "revenue": revenue,
        "low_stock": low,
        "recent": orders.order_by("-created_at")[:10],
    })
