from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# Create an OrderItem Inline
class OrderItemInline(admin.StackedInline):
    # model to add
    model = OrderItem
    extra = 0   #nak tnya item yang ada dalam order shj
#extend our Order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]  # untuk tunjuk readonly field
    # fields = ["user", "full_name", "email", "shipping_address", "amount_paid"] # kalau nak pilih certain field
    inlines = [OrderItemInline]

#Unregister Order Model
admin.site.unregister(Order)

# Re-Register our Order and OrderItem
admin.site.register(Order, OrderAdmin)