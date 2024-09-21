from django.test import TestCase

# Create your tests here.
from decimal import Decimal
from django.test import TestCase

from .models import Receipt


class ReceiptTest(TestCase):

    def test_receipt(self):
        total = 37.55

        expected = 37.55
        self.assertEqual(expected, total)
