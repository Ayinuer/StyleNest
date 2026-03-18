from django.test import TestCase
from category.models import Category
from .models import Product


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            category_name='Women',
            slug='women',
            description='Women fashion category'
        )

        self.product = Product.objects.create(
            product_name='Red Dress',
            slug='red-dress',
            description='Beautiful red dress',
            price=49.99,
            stock=10,
            is_available=True,
            category=self.category
        )

    def test_product_creation(self):
        self.assertEqual(self.product.product_name, 'Red Dress')

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Red Dress')

    def test_product_category(self):
        self.assertEqual(self.product.category.category_name, 'Women')

# Create your tests here.
