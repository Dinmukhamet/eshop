from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from core.models import *
from .factories import *
# Create your tests here.


class ModelTest(TestCase):
    def setUp(self):
        self.name = 'Test'
        self.brand = BrandFactory()
        self.category = Category.objects.create(name=self.name)
        self.product = ProductFactory()
        # self.price = Price.objects.create(product=self.product, price=250)
        self.purchase = Purchase.objects.create()
        self.purchased_product = PurchasedProduct.objects.create(
            purchase=self.purchase, product=self.product, count=2)
    #     self.sale = Sale.objects.create(value=20)
    #     # self.sale.products.add(self.product)
        self.customerinfo = CustomerInfo.objects.create(name=self.name)
        self.rating = Rating.objects.create(product=self.product, rate=5)
        self.comment = Comment.objects.create(
            product=self.product, comment='test')
        self.comment_rating = CommentRating.objects.create(
            comment=self.comment, rate=5)
        self.slider = Slider.objects.create()
        self.recommended_product = RecommendedProduct.objects.create(category=self.category)
        self.sale = Sale.objects.create()
        self.product_to_sale = ProductToSale.objects.create(sale=self.sale, category=self.category, product=self.product)

    def test_brand(self):
        self.assertEqual(self.brand.__str__(), self.brand.name)

    def test_category(self):
        self.assertEqual(self.category.__str__(), self.name)

    def test_product(self):
        self.assertEqual(self.product.__str__(), self.product.name)

    def test_display_customer_info(self):
        customer_name = [customer.name for customer in self.purchase.contacts.all()]
        self.assertEqual(self.purchase.display_customer_info(), ', '.join(customer_name)[:3])
    
    def test_display_customer_phonenumber(self):
        customer_phonenumber = [customer.phone_number for customer in self.purchase.contacts.all()]
        self.assertEqual(self.purchase.display_customer_phonenumber(), ', '.join(customer_phonenumber)[:3])
    
    def test_display_customer_email(self):
        customer_email = [customer.email for customer in self.purchase.contacts.all()]
        self.assertEqual(self.purchase.display_customer_email(), ', '.join(customer_email)[:3])
   
    def test_display_customer_address(self):
        customer_address = [customer.address for customer in self.purchase.contacts.all()]
        self.assertEqual(self.purchase.display_customer_address(), ', '.join(customer_address)[:3])
    
    def test_display_purchased_product(self):
        product_data = [product.product.name for product in self.purchase.products.all()]
        product_count = [product.count for product in self.purchase.products.all()]
        mydict = dict(zip(product_data, product_count))
        self.assertEqual(self.purchase.display_purchased_product(), ', '.join(['%s: %s' % (key, value) for (key, value) in mydict.items()]))
    
    # def test_product_get_id(self):
    #     self.assertEqual(self.product.get_id(), self.product.id)

    # # def test_product_current_price(self):
    # #     price = self.product.price.order_by('-created_at')[0].price
    # #     self.assertEqual(self.product.current_price, price)

    # def test_price(self):
    #     string = 'Product {}: {}'.format(self.product.name, self.price)
    #     self.assertEqual(self.price.__str__(), string)

    # def test_purchase_total_sum(self):
    #     total_sum = sum(item.total() for item in self.purchased_product.__class__.objects.filter(
    #         purchase=self.purchase))
    #     self.assertEqual(self.purchase.total_sum(), total_sum)

    def test_purchased_product(self):
        string = 'Purchase #{}: {} - {}'.format(self.purchase.id, self.product.name, self.purchased_product.count)
        self.assertEqual(self.purchased_product.__str__(), string)

    # def test_purchased_product_name(self):
    #     self.assertEqual(self.purchased_product.name(), self.product.name)

    # def test_purchased_product_sale(self):
    #     self.assertEqual(self.purchased_product.sale_value(), self.sale.value)
    #     Sale.objects.filter(id=self.sale.id).delete()
    #     self.assertEqual(self.purchased_product.sale_value(), 0)

    def test_customerinfo(self):
        self.assertEqual(self.customerinfo.__str__(), self.customerinfo.name)

    def test_rating(self):
        self.assertEqual(self.rating.__str__(), '{}: {}'.format(
            self.product.name, self.rating.rate))

    def test_comment(self):
        self.assertEqual(self.comment.__str__(), '{}: {}'.format(
            self.product.name, self.comment.comment))

    def test_comment_rating(self):
        self.assertEqual(self.comment_rating.__str__(
        ), 'Comment to product "{}" #{} - {}'.format(self.product, self.comment, self.comment_rating.rate))

    def test_slider(self):
        self.assertEqual(self.slider.__str__(
        ), 'There is no product. Slider #{}'.format(self.slider.id))
        self.slider.product = self.product
        self.assertEqual(self.slider.__str__(),
                         'Images for product {}'.format(self.product.name))

    def test_recommended_product(self):
        self.assertEqual('Recommended Product object #{}'.format(
        self.recommended_product.id), self.recommended_product.__str__())
    
    def test_display_recommendedproduct(self):
        self.assertEqual(self.recommended_product.display_recommendedproduct(),
        ', '.join(product.name for product in self.recommended_product.product.all()[:3]))

    def test_sale(self):
        self.assertEqual(self.sale.__str__(), str(self.sale.value) + '%')

    def test_display_products_to_sale(self):
        self.assertEqual(self.sale.display_products_to_sale(), ', '.join(product.product_name() for product in self.sale.products.all()[:3]))


    def test_producttosale_product_name(self):
        self.assertEqual(self.product.name , self.product_to_sale.product_name())

    def test_producttosale_old_price(self):
        self.assertEqual(self.product.price, self.product_to_sale.old_price())

    def test_producttosale_new_price(self):
        price = self.product.price
        new_price = price - (price * self.sale.value / 100)
        self.assertEqual(self.product_to_sale.new_price(), new_price)

class SerializerTest(APITestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.category = CategoryFactory()

    def test_purchase_create(self):
        # Price.objects.create(product=product, price=150)

        url = reverse('purchase')
        data = {
            "contacts": [
                {
                    "name": "Dimash",
                    "email": "d.igisinov@gmail.com",
                    "phone_number": "+996552206521",
                    "address": "test"
                }
            ],
            "products": [
                {
                    "product": self.product.id,
                    "count": 2
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_sale_create(self):
        url = reverse('sales')
        data = {
            "products": [
                {
                    "category": self.category.id,
                    "product": self.product.id
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)