from django.db import models

from django.contrib.auth.models import User
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Product(models.Model):
    STOCK_CHOICES = [
        ('out_of_stock', 'Out of stock'),
        ('low_stock', 'Low stock'),
        ('in_stock', 'In stock'),
    ]
    name = models.CharField(max_length=200)
    Color = models.CharField(max_length=200)
    Material = models.CharField(max_length=200)
    Brand = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='photos/%y/%m/%d',default='photos/24/07/29/home4.png')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    stock = models.CharField(max_length=20, choices=STOCK_CHOICES, default='in_stock')
   #كميه المنتج المتوفره 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def get_average_rating(self):
        ratings = self.ratings.all() 
        if ratings.exists():
            return ratings.aggregate(average_rating=models.Avg('score'))['average_rating']
        return None

    def __str__(self):
        return self.name
    
    class Meta:
     ordering =['-name']
    

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} - {self.score}'

    class Meta:
        ordering = ['-created_at']




class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    order_status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()