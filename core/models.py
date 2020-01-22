from django.db import models

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(
        upload_to='product_pics/', default='product_pics/None/no-img.jpg')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{}: {}'.format(self.name, self.price)


class SubcategoryToProduct(models.Model):
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)

    class Meta:
        ordering = ['subcategory']

    def __str__(self):
        subcategory_name = self.subcategory.name
        product_name = self.product.name
        return '{}: {}'.format(subcategory_name, product_name)


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
        ordering = ['purchase']

    def name(self):
        return self.product.name

    def price(self):
        return self.product.price

    def total(self):
        return self.count * self.price()


class Contact(models.Model):
    purchase = models.ForeignKey(
        Purchase, related_name='contacts', on_delete=models.CASCADE, default=True, null=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    comment = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
