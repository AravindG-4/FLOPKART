import os
from Flopkart.settings import MEDIA_ROOT
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class Signup(models.Model):
#   username = models.CharField(max_length=100)
#   email = models.EmailField()
#   password = models.CharField(max_length=100)

# class login(models.Model):
#   username = models.CharField(max_length=100)
#   email = models.EmailField()
#   password = models.CharField(max_length=100)


class Product(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]
    
    name=models.CharField(max_length=255)
    description=models.CharField(max_length=100)
    available_count=models.PositiveIntegerField()
    category= models.ForeignKey('Category', on_delete=models.CASCADE)
    sub_category = models.ForeignKey('SubCategory', on_delete = models.CASCADE)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, default='M')
    colour = models.CharField(max_length=255, default='Not Mentioned')
    brand = models.ForeignKey('Brand', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    discount = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    actual_price = models.DecimalField(max_digits = 10,decimal_places = 5)
    available_price = models.DecimalField(max_digits = 10,decimal_places = 5)
    is_active = models.BooleanField(default = True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.available_price = self.actual_price - (self.actual_price * self.discount / 100)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

class Category(models.Model):
    name=models.CharField(max_length=25)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return str(self.name)
      
class SubCategory(models.Model):
    name_sub=models.CharField(max_length=25)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
      return self.name_sub

def brand_logo_path(instance, filename):
    brand_name = instance.name.lower().replace(' ', '_')
    
    return os.path.join('brand_logos', f'{brand_name}{os.path.splitext(filename)[1]}')

class Brand(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to=brand_logo_path, blank=True)
    description = models.TextField(blank=True)
    top_categories = models.ManyToManyField('Category', related_name='cats', blank=True)
    top_subCategories = models.ManyToManyField('SubCategory', related_name='subCats', blank=True)
    
    def __str__(self):
        return self.name

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    
    def __str__(self):
      return str(self.user.name)
    
    
def product_image_path(instance, filename):
    product_name = instance.product.name.replace(' ', '_')
    product_images_dir = os.path.join('images', product_name)
    
    os.makedirs(os.path.join(MEDIA_ROOT, product_images_dir), exist_ok=True)
    
    existing_files = os.listdir(os.path.join(MEDIA_ROOT, product_images_dir))
    
    new_filename = str(len(existing_files) + 2) + os.path.splitext(filename)[1]

    return os.path.join(product_images_dir, new_filename)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_path)

    def __str__(self):
        return str(self.image)
