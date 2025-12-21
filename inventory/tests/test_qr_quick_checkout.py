from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from inventory.models import StockItem, CheckoutRecord
from django.utils import timezone

User = get_user_model()

class QRQuickCheckoutTests(TestCase):
    def setUp(self):
        # create a student user and a stock item
        self.student = User.objects.create_user(username='student1', password='pass123')
        self.item = StockItem.objects.create(name='Test Multimeter', sku='TM-001')

    def test_quick_checkout_requires_login(self):
        url = reverse('inventory:quick_checkout', args=[str(self.item.qr_token)])
        resp = self.client.get(url)
        # should redirect to login
        self.assertEqual(resp.status_code, 302)

    def test_quick_checkout_post_creates_checkout(self):
        self.client.login(username='student1', password='pass123')
        url = reverse('inventory:quick_checkout', args=[str(self.item.qr_token)])
        resp = self.client.post(url, {'due_days': 3})
        self.assertEqual(resp.status_code, 200)
        co = CheckoutRecord.objects.filter(item=self.item, student=self.student).first()
        self.assertIsNotNone(co)
        self.assertEqual(co.status, 'out')
        # due_date roughly now + 3 days
        delta = co.due_date - timezone.now()
        self.assertTrue(2 <= delta.days <= 4)
