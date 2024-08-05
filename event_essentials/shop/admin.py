from django.contrib import admin

# Register your models here.
from .models import Product, Contact, Orders, OrderUpdate,RentInfo,signup,ThemeProduct


admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
admin.site.register(signup)
admin.site.register(RentInfo)
admin.site.register(ThemeProduct)
# admin.site.register(OrderHistory)

# admin.site.register(ThemeOrderUpdate)