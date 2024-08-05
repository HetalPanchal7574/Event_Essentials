from django.db import models
from unittest.util import _MAX_LENGTH

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50,default="")
    # subcategory = models.CharField(max_length=50,default="")
    rent_price = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    # desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    # product_qty = models.IntegerField(default=0)
    image = models.ImageField(upload_to="shop/images",default="")
    
    def __str__(self):
         return f"{self.product_id} - {self.product_name}"

class Contact(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)
    email = models.CharField(max_length=70,default="")
    phone_no = models.CharField(max_length=70,default="")
    desc = models.CharField(max_length=500, default="")
    
    def __str__(self):
        return self.name
    
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=20,default="") 
    email = models.CharField(max_length=70,default="") 
    address = models.CharField(max_length=200) 
    city = models.CharField(max_length=20) 
    state = models.CharField(max_length=20) 
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=12) 
    
   
class OrderUpdate(models.Model):
    update_id= models.AutoField(primary_key=True)
    order_id= models.IntegerField(default="")
    update_desc= models.CharField(max_length=5000)
    timestamp= models.DateField(auto_now_add= True)
    email = models.CharField(max_length=70,default="") 

def _str_(self):
    return self.update_desc[0:7] + "..."

#   


class RentInfo(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)  # Assuming you're storing phone number as a string
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    need_extra_info = models.BooleanField(default=False)
    extra_info_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class signup(models.Model):
    firstname = models.CharField(max_length=50,default="")
    lastname = models.CharField(max_length=50,default="")
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    passwd = models.CharField(max_length=16)
    city = models.CharField(max_length=50,default="")
    state = models.CharField(max_length=50,default="")
    phone_no = models.CharField(max_length=12,default="")

    def __str__(self) -> str:
        return self.email


class ThemeProduct(models.Model):
    theme_product_id = models.AutoField(primary_key=True)
    theme_product_name = models.CharField(max_length=50)
    theme_category = models.CharField(max_length=50,default="")
    # subcategory = models.CharField(max_length=50,default="")
    theme_rent_price = models.IntegerField(default=0)
    theme_price = models.IntegerField(default=0)
    # desc = models.CharField(max_length=300)
    theme_pub_date = models.DateField()
    # product_qty = models.IntegerField(default=0)
    theme_image = models.ImageField(upload_to="shop/images",default="")
    
    def __str__(self):
         return f"{self.theme_product_id} - {self.theme_product_name}"
    


# class OrderHistory(models.Model):
#     product_id = models.IntegerField()
#     product_name = models.CharField(max_length=255)
#     email_id = models.EmailField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     product_type = models.CharField(max_length=50)
#     date = models.DateTimeField(auto_now_add=True)
#     extra_info = models.TextField(null=True, blank=True)  # Add this field for additional variable
