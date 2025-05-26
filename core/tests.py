from django.test import TestCase
from core.models import Instrument

class InstrumentModelTest(TestCase):
    def test_instrument_creation(self):
        instrument = Instrument.objects.create(label="Test Instrument", instrument_type_id=1) # Assuming InstrumentType exists with ID 1
        self.assertEqual(instrument.label, "Test Instrument")