from django.db import models
from django.db.models import Sum
from django.core.validators import MaxValueValidator, MinValueValidator
# from annoying.fields import AutoOneToOneField
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
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=254, default='https://imgur.com/bY5YJhB')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=False)
    category = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    total_purchase = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)

    # @property
    # def current_price(self):
    #     if self.price.all():
    #         return self.price.order_by('-created_at')[0].price

# class Price(models.Model):
#     product = models.ForeignKey(Product, related_name='price', on_delete=models.CASCADE, null=False)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
#     date_to = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         product_name = self.product.name
#         return 'Product {}: {}'.format(product_name, self.price)


class Purchase(models.Model):
    # date = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     ordering = ['date']

    def total_sum(self):
        return sum(item.total() for item in PurchasedProduct.objects.filter(purchase=self.id))


class PurchasedProduct(models.Model):
    purchase = models.ForeignKey(
        Purchase, related_name='products', on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['product']

    def __str__(self):
        purchase_id = self.id
        product_name = self.product.name
        return 'Purchase #{}: {} - {}'.format(purchase_id, product_name, self.count)

    def name(self):
        return self.product.name

    def price(self):
        return float(self.product.price)   

    def sale_value(self):
        if Sale.objects.filter(products=self.product):
            return Sale.objects.get(products=self.product).value
        else:
            return 0

    def total(self):
        sale = self.count * self.price() * (self.sale_value() / 100)
        return (self.count * self.price()) - sale

    def save(self, *args, **kwargs):
        product = self.product
        product.total_purchase += self.count
        product.save()
        super(PurchasedProduct, self).save(*args, **kwargs)


class CustomerInfo(models.Model):
    purchase = models.ForeignKey(
        Purchase, related_name='contacts', on_delete=models.CASCADE, null=True)
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
    rate = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['product']

    def __str__(self):
        product_name = self.product.name
        return '{}: {}'.format(product_name, self.rate)


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    comment = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['product']

    def __str__(self):
        product_name = self.product.name
        return '{}: {}'.format(product_name, self.comment)


class CommentRating(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=False)
    rate = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['comment']

    def __str__(self):
        product = self.comment.product.name
        return 'Comment to product "{}" #{} - {}'.format(product, self.comment, self.rate)


class Slider(models.Model):
    image = models.URLField(max_length=254, default='https://imgur.com/ bY5YJhB')
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['image']

    def __str__(self):
        if self.product:
            product_name = self.product.name
            return 'Images for product {}'.format(product_name)
        return 'There is no product. Slider #{}'.format(self.id)


class RecommendedProduct(models.Model):
    date_from = models.DateTimeField(auto_now_add=True)
    date_to = models.DateTimeField(null=True, blank=True)
    products = models.ManyToManyField(Product)

    class Meta:
        ordering = ['date_from']

    def __str__(self):
        return 'Recommended Product object #{}'.format(self.id)


class Sale(models.Model):
    date_from = models.DateTimeField(null=True, blank=True)
    date_to = models.DateTimeField(null=True, blank=True)
    value = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_from']

class ProductToSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    sale = models.ForeignKey(Sale, related_name='products', on_delete=models.CASCADE, null=False)

    class Meta:
        ordering = ['product']
    
    def old_price(self):
        return self.product.price

    def new_price(self):
        price = old_price()
        sale_value = self.sale.value
        return price - (price * sale_value / 100)
    


class SaleSummary(PurchasedProduct):
    
    class Meta:
        proxy = True
        verbose_name = 'Sale Summary'
        verbose_name_plural = 'Sales Summary'
