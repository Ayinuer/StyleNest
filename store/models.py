from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from category.models import Category

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='photos/products', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

class Variation(models.Model):
    VARIATION_CATEGORY_CHOICES = (
        ('color', 'color'),
        ('size', 'size'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    variation_category = models.CharField(max_length=100, choices=VARIATION_CATEGORY_CHOICES)
    variation_value = models.CharField(max_length=100) # e.g., "Midnight Blue" or "XL"
    
    # New field for Hex Codes (e.g., #0000FF)
    color_code = models.CharField(max_length=7, blank=True, null=True, help_text="Enter Hex code (e.g. #FFFFFF) for color variations")
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.variation_category}: {self.variation_value}"

class ProductAttribute(models.Model):
    """
    The SKU model. Tracks stock for specific combinations.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # This links a specific SKU to both a Color Variation and a Size Variation
    variations = models.ManyToManyField(Variation)
    sku = models.CharField(max_length=50, unique=True)
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.product.product_name} [{self.sku}]"
