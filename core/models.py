from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from smart_selects.db_fields import ChainedForeignKey, ChainedManyToManyField
from rest_framework.exceptions import APIException
import random
from django.utils.translation import ugettext_lazy as _

# from .storage import OverwriteStorage
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
    name = models.CharField(max_length=255, verbose_name=_('Name'))

    class Meta:
        ordering = ['name']
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    # parent = models.ForeignKey(
    # 'self', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=False, verbose_name=_('Category'))

    class Meta:
        ordering = ['name']
        verbose_name = _('Subcategory')
        verbose_name_plural = _('Subcategories')

    def __str__(self):
        return self.name


def upload_location(instance, filename):
    filebase, extension = filename.rsplit('.', 1)
    if extension == 'webp':
        raise APIException('Choose another image format')
    else:
        return 'product_images/%032x.%s' % (random.getrandbits(128), extension)


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_('Price'))
    image = models.ImageField(
        upload_to=upload_location, verbose_name=_('Image'))
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, null=False, verbose_name=_('Brand'))
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=False, verbose_name=_('Category'))
    subcategory = ChainedForeignKey(
        Subcategory,
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=True,
        sort=True,
        verbose_name=_('Subcategory'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date'))
    total_purchase = models.PositiveIntegerField(
        default=0, verbose_name=_('Total Purchase'))

    class Meta:
        ordering = ['name']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

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


class ProductImages(models.Model):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE, null=False, verbose_name=_('Product'))
    image = models.ImageField(
        upload_to=upload_location, verbose_name=_('Image'))

    class Meta:
        ordering = ['id']
        verbose_name = _('Product image')
        verbose_name_plural = _('Product images')


class Purchase(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date created'))

    class Meta:
        verbose_name = _('Purchase')
        verbose_name_plural = _('Purchases')

    def total_sum(self):
        return sum(item.total() for item in PurchasedProduct.objects.filter(purchase=self.id))

    total_sum.short_description = _('Total')

    def display_customer_info(self):
        return ', '.join(customer.name for customer in self.contacts.all()[:3])

    display_customer_info.short_description = _('Customer')

    def display_customer_email(self):
        return ', '.join(customer.email for customer in self.contacts.all()[:3])

    display_customer_email.short_description = _('Email')

    def display_customer_phonenumber(self):
        return ', '.join(customer.phone_number for customer in self.contacts.all()[:3])

    display_customer_phonenumber.short_description = _('Phone number')

    def display_customer_address(self):
        return ', '.join(customer.address for customer in self.contacts.all()[:3])

    display_customer_address.short_description = _('Address')

    def display_purchased_product(self):
        product_data = [
            product.product.name for product in self.products.all()]
        product_count = [product.count for product in self.products.all()]
        mydict = dict(zip(product_data, product_count))
        return ', '.join(['%s: %s' % (key, value) for (key, value) in mydict.items()])

    display_purchased_product.short_description = _('Purchased products')


class PurchasedProduct(models.Model):
    purchase = models.ForeignKey(
        Purchase, related_name='products', on_delete=models.CASCADE, null=False, verbose_name=_('Purchase'))
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, verbose_name=_('Product'))
    count = models.IntegerField(verbose_name=_('Quantity'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date created'))

    class Meta:
        ordering = ['product']
        verbose_name = _('Purchased product')
        verbose_name_plural = _('Purchased products')

    def __str__(self):
        purchase_id = self.id
        product_name = self.product.name
        return 'Purchase #{}: {} - {}'.format(purchase_id, product_name, self.count)

    def name(self):
        return self.product.name

    name.short_description = _('Name of the product')

    def price(self):
        return float(self.product.price)

    price.short_description = _('Price')

    def sale_value(self):
        try:
            product = ProductToSale.objects.get(
                product=self.product).sale.value
        except ProductToSale.DoesNotExist:
            product = 0
        return product

    sale_value.short_description = _('Discount')

    def total(self):
        sale = self.count * self.price() * (self.sale_value() / 100)
        return (self.count * self.price()) - sale

    total.short_description = _('Total')

    def save(self, *args, **kwargs):
        product = self.product
        product.total_purchase += self.count
        product.save()
        super(PurchasedProduct, self).save(*args, **kwargs)


class CustomerInfo(models.Model):
    purchase = models.ForeignKey(
        Purchase, related_name='contacts', on_delete=models.CASCADE, null=True, verbose_name=_('Purchase'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    email = models.EmailField(max_length=255, verbose_name=_('Email'))
    phone_number = models.CharField(
        max_length=255, verbose_name=_('Phone number'))
    address = models.CharField(max_length=255, verbose_name=_('Address'))
    comment = models.TextField(blank=True, verbose_name=_('Comment'))

    class Meta:
        ordering = ['name']
        verbose_name = _('Customer info')
        verbose_name_plural = _('Customers info')

    def __str__(self):
        return self.name


class Rating(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, verbose_name=_('Product'))
    rate = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name=_('Rate'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date created'))

    class Meta:
        ordering = ['product']
        verbose_name = _('Product rate')
        verbose_name_plural = _('Rates of products')

    def __str__(self):
        product_name = self.product.name
        return '{}: {}'.format(product_name, self.rate)


class Comment(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, verbose_name=_('Product'))
    comment = models.TextField(blank=False, verbose_name=_('Comment'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date created'))

    class Meta:
        ordering = ['product']
        verbose_name = _('Comment to product')
        verbose_name_plural = _('Comment to products')

    def __str__(self):
        product_name = self.product.name
        return '{}: {}'.format(product_name, self.comment)


class CommentRating(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, null=False, verbose_name=_('Comment'))
    rate = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name=_('Rate'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date created'))

    class Meta:
        ordering = ['comment']
        verbose_name = _('Rating for comment')
        verbose_name_plural = _('Ratings for comments')

    def __str__(self):
        product = self.comment.product.name
        return 'Comment to product "{}" #{} - {}'.format(product, self.comment, self.rate)


class RecommendedProduct(models.Model):
    date_from = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date from'))
    date_to = models.DateTimeField(
        null=True, blank=True, verbose_name=_('Date to'))
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=False, verbose_name=_('Category'))
    subcategory = ChainedForeignKey(
        Subcategory,
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=True,
        sort=True,
        verbose_name=_('Subcategory'))
    product = ChainedManyToManyField(
        Product,
        chained_field="subcategory",
        chained_model_field="subcategory",
    )

    class Meta:
        ordering = ['date_from']
        verbose_name = _('Recommended product')
        verbose_name_plural = _('Recommended products')

    def __str__(self):
        return 'Recommended Product object #{}'.format(self.id)

    def display_recommendedproduct(self):
        return ', '.join(product.name for product in self.product.all()[:3])

    display_recommendedproduct.short_description = _('Products')


# class ProductToRecommendedProduct(models.Model):
#     recommended_product = models.ForeignKey(
#         RecommendedProduct, related_name='products', on_delete=models.CASCADE, null=False)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)

#     class Meta:
#         ordering = ['recommended_product']


class Sale(models.Model):
    date_from = models.DateTimeField(
        null=True, blank=True, verbose_name=_('Date from'))
    date_to = models.DateTimeField(
        null=True, blank=True, verbose_name=_('Date to'))
    value = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name=_('Value'))
    created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date created'))

    class Meta:
        ordering = ['date_from']
        verbose_name = _('Discount')
        verbose_name_plural = _('Discounts')

    def __str__(self):
        return str(self.value) + '%'

    def display_products_to_sale(self):
        return ', '.join(product.product_name() for product in self.products.all()[:3])

    display_products_to_sale.short_description = _('Products')


class ProductToSale(models.Model):
    sale = models.ForeignKey(
        Sale, related_name='products', on_delete=models.CASCADE, null=False, verbose_name=_('Discount'))

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=False, verbose_name=_('Category'))
    subcategory = ChainedForeignKey(
        Subcategory,
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=True,
        sort=True,
        verbose_name=_('Subcategory'))
    product = ChainedForeignKey(
        Product,
        chained_field="subcategory",
        chained_model_field="subcategory",
        show_all=False,
        auto_choose=True,
        sort=True,
        verbose_name=_('Product'))

    class Meta:
        ordering = ['product']
        verbose_name = _('Product with discount')
        verbose_name_plural = _('Products with discounts')

    def product_name(self):
        return self.product.name

    product_name.short_description = _('Product')

    def old_price(self):
        return self.product.price

    old_price.short_description = _('Old price')

    def new_price(self):
        price = self.old_price()
        sale_value = self.sale.value
        return price - (price * sale_value / 100)

    new_price.short_description = _('New price')

    def save(self, *args, **kwargs):
        if ProductToSale.objects.filter(product=self.product).count() >= 1:
            raise Exception("This product already has a discount")
        else:
            super().save(*args, **kwargs)


class SaleSummary(PurchasedProduct):

    class Meta:
        proxy = True
        verbose_name = _('Sale Summary')
        verbose_name_plural = _('Sales Summary')


class SaleBundle(models.Model):
    date_from = models.DateTimeField(
        null=True, blank=True, verbose_name=_('Date from'))
    date_to = models.DateTimeField(
        null=True, blank=True, verbose_name=_('Date to'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date created'))
    description = models.TextField(verbose_name=_('Description'))
    price = models.IntegerField(default=0, verbose_name=_('Price'))

    class Meta:
        ordering = ['date_from']
        verbose_name = _('Sale')
        verbose_name_plural = _('Sales')

    def total_price(self):
        return sum(product.product.price for product in self.products.all())

    total_price.short_description = _('Old price')

    def new_price(self):
        if self.price == 0:
            data = [product.product.price for product in self.products.all()]
            data.remove(min(data))
            return sum(data)
        else:
            return self.price

    new_price.short_description = _('New price')

    def display_products(self):
        return ', '.join(product.product.name for product in self.products.all())

    display_products.short_description = _('Products')


class ProductToSaleBundle(models.Model):
    salebundle = models.ForeignKey(
        SaleBundle, related_name='products', on_delete=models.CASCADE, null=False, verbose_name=_('Sale'))
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=False, verbose_name=_('Category'))
    subcategory = ChainedForeignKey(
        Subcategory,
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=True,
        sort=True,
        verbose_name=_('Subcategory'))
    product = ChainedForeignKey(
        Product,
        chained_field="subcategory",
        chained_model_field="subcategory",
        show_all=False,
        auto_choose=True,
        sort=True,
        verbose_name=_('Product'))

    class Meta:
        ordering = ['salebundle']
        verbose_name = _('Product on sale')
        verbose_name_plural = _('Products on sale')

    def price(self):
        return self.product.price

    price.short_description = _('Price')


class Slider(models.Model):
    image = models.ImageField(
        upload_to='slider_images', verbose_name=_('Image'))
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Product'))
    salebundle = models.ForeignKey(
        SaleBundle, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Sale'))
    description = models.TextField(verbose_name=_('Description'))

    class Meta:
        ordering = ['image']
        verbose_name = _('Slider')
        verbose_name_plural = _('Slider')

    def display_product_in_salebundle(self):
        if self.salebundle:
            return self.salebundle.display_products()
        else:
            return None

    display_product_in_salebundle.short_description = _('Products on sale')

    def product_name(self):
        if self.product:
            return self.product.name
        else:
            return None

    product_name.short_description = _('Product name')


class FooterMedia(models.Model):
    name = models.CharField(max_length=254)
    media_type = models.URLField(max_length=254)
    image = models.ImageField(upload_to='footer_images')

    class Meta:
        ordering = ['name']
        verbose_name = _('Footer link')
        verbose_name_plural = _('Footer links')

    def __str__(self):
        return self.name
