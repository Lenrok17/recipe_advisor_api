from django.db import models

class Unit(models.TextChoices):
    GRAM = 'g', 'Gram'
    KILOGRAM = 'kg', 'Kilogram'
    MILLILITER = 'ml', 'Milliliter'
    LITER = 'l', 'Liter'
    PIECE = 'pcs', 'Piece'
    TEASPOON = 'tsp', 'Teaspoon'
    TABLESPOON = 'tbsp', 'Tablespoon'

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, blank=True, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name