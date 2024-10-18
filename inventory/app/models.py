from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null= True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    
class Supplier(models.Model):
    name = models.CharField(max_length=200)
    number = models.IntegerField()
    email = models.EmailField(null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='productsCategory',null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='productsUser')
    suppliers = models.ManyToManyField(Supplier, related_name='productsSupplier', blank=True,null=True,through='ProductSuppliers')
    
class ProductSuppliers(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    supplier = models.ForeignKey('Supplier',on_delete=models.CASCADE)
    supply = models.PositiveIntegerField(blank=True,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('product', 'supplier')
    

    
    
