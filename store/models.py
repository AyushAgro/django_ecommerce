from django.db import models
from django.urls import reverse
from category.models import Category

# Create your models here.
class Product(models.Model):
  product_name  = models.CharField(max_length=200, unique=True)
  slug = models.SlugField(max_length = 200, unique = True)
  description = models.TextField(max_length=200 , blank = True)
  image = models.ImageField(upload_to='photos/product')
  stock = models.IntegerField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  is_available = models.BooleanField(default=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.product_name

  def get_url(self):
    return reverse('product_detail', args = [
      self.category.slug, self.slug
    ])

class VaritationManager(models.Manager):
  def color(self):
    return super(VaritationManager, self).filter(variation_category = 'color', is_active = True)

  def size(self):
    return super(VaritationManager, self).filter(variation_category = 'size', is_active = True)


class Variation(models.Model):
  variation_cat_choice = (
    ('color', 'color'),
    ('size', 'size')
  )
  product = models.ForeignKey(Product, on_delete = models.CASCADE)
  variation_category = models.CharField(max_length=20, choices = variation_cat_choice)
  variation_values = models.CharField(max_length=50)
  is_active = models.BooleanField(default=True)

  object = VaritationManager()

  def __str__(self):
    return self.variation_values
