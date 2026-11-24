from decimal import Decimal

from django.test import TestCase, Client
from django.urls import reverse

from shop.models import Product, Purchase


class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_webpage_accessibility(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class PromoCodeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(name='Машинка', price=499)

    def order(self, **fields):
        return self.client.post(
            reverse('buy', args=[self.product.pk]),
            {'person': 'Иван', 'address': 'Тестовый адрес', **fields},
            follow=True,
        )

    def test_form_shows_selected_product(self):
        response = self.client.get(reverse('buy', args=[self.product.pk]))
        self.assertContains(response, 'Машинка')
        self.assertContains(response, 'name="promo_code"')

    def test_three_discounts(self):
        for code, price in (
            ('TOY5', '474.05'), ('TOY10', '449.10'), ('TOY15', '424.15'),
        ):
            with self.subTest(code=code):
                response = self.order(promo_code=code)
                self.assertRedirects(response, reverse('index'))
                self.assertContains(response, f'К оплате {price} ₽')
                purchase = Purchase.objects.get(promo_code=code)
                self.assertEqual(purchase.total_price, Decimal(price))

    def test_normalizes_promo_code(self):
        self.order(promo_code=' toy10 ')
        self.assertEqual(Purchase.objects.get().promo_code, 'TOY10')

    def test_purchase_without_code_keeps_full_price(self):
        self.order()
        purchase = Purchase.objects.get()
        self.assertEqual(purchase.promo_code, '')
        self.assertEqual(purchase.total_price, Decimal('499.00'))

    def test_invalid_promo_code_does_not_create_purchase(self):
        response = self.order(promo_code='UNKNOWN')
        self.assertFormError(response.context['form'], 'promo_code',
                             'Такого промокода нет.')
        self.assertFalse(Purchase.objects.exists())

    def test_uses_product_from_url(self):
        other_product = Product.objects.create(name='Медведь', price=800)
        self.order(product=other_product.pk, total_price='0.01')
        purchase = Purchase.objects.get()
        self.assertEqual(purchase.product, self.product)
        self.assertEqual(purchase.total_price, Decimal('499.00'))

    def test_missing_product_returns_404(self):
        response = self.client.get(reverse('buy', args=[self.product.pk + 1]))
        self.assertEqual(response.status_code, 404)
