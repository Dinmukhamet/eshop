from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from smart_selects.db_fields import ChainedForeignKey, ChainedManyToManyField


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
    # parent = models.ForeignKey(
    # 'self', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(
        max_length=254, default='https://imgur.com/bY5YJhB')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=False)
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    total_purchase = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)

    def total_quantity(self):
        return Product.objects.all().count()

    def category(self):
        return self.subcategory.category.id
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

    def display_customer_info(self):
        return ', '.join(customer.name for customer in self.contacts.all()[:3])

    display_customer_info.short_description = 'Customer'

    def display_customer_email(self):
        return ', '.join(customer.email for customer in self.contacts.all()[:3])

    display_customer_email.short_description = 'Email'

    def display_customer_phonenumber(self):
        return ', '.join(customer.phone_number for customer in self.contacts.all()[:3])

    display_customer_phonenumber.short_description = 'Phone number'

    def display_customer_address(self):
        return ', '.join(customer.address for customer in self.contacts.all()[:3])

    display_customer_address.short_description = 'Address'

    def display_purchased_product(self):
        product_data = [
            product.product.name for product in self.products.all()]
        product_count = [product.count for product in self.products.all()]
        mydict = dict(zip(product_data, product_count))
        return ', '.join(['%s: %s' % (key, value) for (key, value) in mydict.items()])

    display_purchased_product.short_description = 'Products'


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
        try:
            product = ProductToSale.objects.get(
                product=self.product).sale.value
        except ProductToSale.DoesNotExist:
            product = 0
        return product

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


class RecommendedProduct(models.Model):
    date_from = models.DateTimeField(auto_now_add=True)
    date_to = models.DateTimeField(null=True, blank=True)
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, null=False)
    product = ChainedManyToManyField(
        Product,
        chained_field="subcategory",
        chained_model_field="subcategory",
    )

    class Meta:
        ordering = ['date_from']

    def __str__(self):
        return 'Recommended Product object #{}'.format(self.id)

    def display_recommendedproduct(self):
        return ', '.join(product.name for product in self.product.all()[:3])

    display_recommendedproduct.short_description = 'Products'


# class ProductToRecommendedProduct(models.Model):
#     recommended_product = models.ForeignKey(
#         RecommendedProduct, related_name='products', on_delete=models.CASCADE, null=False)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)

#     class Meta:
#         ordering = ['recommended_product']


class Sale(models.Model):
    date_from = models.DateTimeField(null=True, blank=True)
    date_to = models.DateTimeField(null=True, blank=True)
    value = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_from']

    def __str__(self):
        return str(self.value) + '%'

    def display_products_to_sale(self):
        return ', '.join(product.product_name() for product in self.products.all()[:3])

    display_products_to_sale.short_description = 'Products'


class ProductToSale(models.Model):
    sale = models.ForeignKey(
        Sale, related_name='products', on_delete=models.CASCADE, null=False)

    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, null=False)
    product = ChainedForeignKey(
        Product,
        chained_field="subcategory",
        chained_model_field="subcategory",
        show_all=False,
        auto_choose=True,
        sort=True)

    class Meta:
        ordering = ['product']

    def product_name(self):
        return self.product.name

    def old_price(self):
        return self.product.price

    def new_price(self):
        price = self.old_price()
        sale_value = self.sale.value
        return price - (price * sale_value / 100)

    def save(self, *args, **kwargs):
        if ProductToSale.objects.filter(product=self.product).count() > 1:
            raise Exception("This product already has a discount")
        else:
            super().save(*args, **kwargs)


class SaleSummary(PurchasedProduct):

    class Meta:
        proxy = True
        verbose_name = 'Sale Summary'
        verbose_name_plural = 'Sales Summary'


class SaleBundle(models.Model):
    date_from = models.DateTimeField(null=True, blank=True)
    date_to = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    class Meta:
        ordering = ['date_from']

    def total_price(self):
        return sum(product.product.price for product in self.products.all())

    def new_price(self):
        data = [product.product.price for product in self.products.all()]
        data.remove(min(data))
        return sum(data)

    def display_products(self):
        return ', '.join(product.product.name for product in self.products.all())

    display_products.short_description = 'Products'


class ProductToSaleBundle(models.Model):
    salebundle = models.ForeignKey(
        SaleBundle, related_name='products', on_delete=models.CASCADE, null=False)
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, null=False)
    product = ChainedForeignKey(
        Product,
        chained_field="subcategory",
        chained_model_field="subcategory",
        show_all=False,
        auto_choose=True,
        sort=True)

    class Meta:
        ordering = ['salebundle']

    def price(self):
        return self.product.price


class Slider(models.Model):
    image = models.URLField(
        max_length=254, default='https://imgur.com/bY5YJhB')
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True)
    salebundle = models.ForeignKey(
        SaleBundle, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['image']
    
    def display_product_in_salebundle(self):
        if self.salebundle:
            return self.salebundle.display_products()
        else:
            return None
    
    def product_name(self):
        if self.product:
            return self.product.name
        else:
            return None