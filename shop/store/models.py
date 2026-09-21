from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.name

class DeliveryZone(models.Model):
    name = models.CharField(max_length=120, unique=True)
    fee = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.name} — {self.fee} FCFA"

class Supplier(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=40, blank=True)
    address = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Driver(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=40)
    vehicle = models.CharField(max_length=120, blank=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    UNIT_CHOICES = [
        ("sac", "Sac"), ("tonne", "Tonne"), ("m3", "m³"),
        ("piece", "Pièce"), ("barre", "Barre"), ("palette", "Palette"),
    ]
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="piece")
    stock = models.PositiveIntegerField(default=0)
    low_stock = models.PositiveIntegerField(default=10)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    def margin(self):
        return self.price - self.purchase_price
    def is_low_stock(self):
        return self.stock <= self.low_stock

class Order(models.Model):
    STATUS = [
        ("pending", "En attente"), ("confirmed", "Confirmée"),
        ("preparing", "En préparation"), ("delivery", "En livraison"),
        ("delivered", "Livrée"), ("cancelled", "Annulée"),
    ]
    PAYMENT = [
        ("cash", "Paiement à la livraison"),
        ("mobile", "Paiement mobile"),
        ("online", "Paiement en ligne"),
    ]
    customer_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100, default="Lomé")
    zone = models.ForeignKey(DeliveryZone, on_delete=models.SET_NULL, null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    delivery_fee = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT, default="cash")
    payment_status = models.CharField(max_length=20, default="pending")
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    def subtotal(self):
        return sum(i.total() for i in self.items.all())
    def grand_total(self):
        return self.subtotal() + self.delivery_fee
    def __str__(self):
        return f"Commande #{self.id} — {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=0)
    def total(self):
        return self.quantity * self.unit_price

class StockMovement(models.Model):
    TYPES = [("in", "Entrée"), ("out", "Sortie"), ("adjust", "Ajustement")]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_movements")
    movement_type = models.CharField(max_length=10, choices=TYPES)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.product} — {self.quantity}"
