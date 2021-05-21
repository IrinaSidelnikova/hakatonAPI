from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Sections(models.Model):
    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=20, primary_key=True)

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=10, primary_key=True)
    image = models.ImageField(upload_to='brands/', null=True, blank=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=20, primary_key=True)
    description = models.TextField()
    image = models.ImageField(upload_to='product/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    section = models.ForeignKey(Sections, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title


class Recall(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='recalls')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recalls')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_time']


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    is_ordered = models.BooleanField(default=False)



