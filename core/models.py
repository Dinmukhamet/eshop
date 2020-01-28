from django.db import models
from django.db.models import Count
from django.core.validators import MaxValueValidator, MinValueValidator 
# Create your models here.


# class IntegerRangeField(models.IntegerField):
#     def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
#         self.min_value, self.max_value = min_value, max_value
#         models.IntegerField.__init__(self, verbose_name, name, **kwargs)

#     def formfield(self, **kwargs):
#         defaults = {'min_value': self.min_value, 'max_value': self.max_value}
#         defaults.update(kwargs)
#         return super(IntegerRangeField, self).formfield(**defaults)


class Brand(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
# setnull chtoby ne udal
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# class Subcategory(models.Model):
#     category = models.ForeignKey(
#         Category, on_delete=models.CASCADE, null=False)
#     parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
#     name = models.CharField(max_length=255)

#     class Meta:
#         ordering = ['name']

#     def __str__(self):
#         return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(default='product_pics/None/no-img.jpg')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=False)
    category = models.ManyToManyField(Category)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{}: {}'.format(self.name, self.price)

    def total_purchase(self):
        return PurchasedProduct.objects.annotate(Count('product'))

# class SubcategoryToProduct(models.Model):
#     subcategory = models.ForeignKey(
#         Subcategory, on_delete=models.CASCADE, null=False)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)

#     class Meta:
#         ordering = ['subcategory']

#     def __str__(self):
#         subcategory_name = self.subcategory.name
#         product_name = self.product.name
#         return '{}: {}'.format(subcategory_name, product_name)


class Purchase(models.Model):
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def total_sum(self):
        return sum(item.total() for item in PurchasedProduct.objects.filter(purchase=self.id))

class PurchasedProduct(models.Model):
    purchase = models.ForeignKey(
        Purchase, related_name='products', on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    count = models.IntegerField()

    class Meta:
        ordering = ['product']
    
    def __str__(self):
        purchase_id = self.id
        product_name = self.product.name
        return 'Purchase #{}: {} - {}'.format(purchase_id, product_name, self.count)

    def name(self):
        return self.product.name

    def price(self):
        return self.product.price

    def total(self):
        return self.count * self.price()
    
class Favourite(models.Model):
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']


class FavouriteProduct(models.Model):
    favourite = models.ForeignKey(
        Favourite, related_name='products', on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)

    class Meta:
        ordering = ['favourite']

    def __str__(self):
        product_name = self.product.name
        return 'Favourite ID: {} - {}'.format(self.favourite, product_name)


class Contact(models.Model):
    purchase = models.ForeignKey(
        Purchase, related_name='contacts', on_delete=models.CASCADE, null=True)
    favourite = models.ForeignKey(
        Favourite, related_name='contacts', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    rate = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        ordering = ['product']

    def __str__(self):
        product_name = self.product.name
        return '{}: {}'.format(product_name, self.rate)

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    comment = models.TextField(blank=False)

    class Meta:
        ordering = ['product']
    
    def __str__(self):
        product_name = self.product.name
        return '{}: {}'.format(product_name, self.comment)

class CommentRating(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=False)
    rate = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        ordering = ['comment']
    
    def __str__(self):
        product = self.comment.product.name
        return 'Comment to product "{}" #{} - {}'.format(product, self.comment, self.rate)

# class Bestseller(models.Model):
#     product = models.ForeignKey(PurchasedProduct, on_delete=models.CASCADE, null=False)

#     class Meta:
#         ordering = ['product']
    
#     def __str__(self):
#         product_name = self.product.name
#         return product_name
    
#     def by_total_purchases(self):
        