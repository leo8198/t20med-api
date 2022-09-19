from datetime import datetime
import random
import string
from database.basic import BasicCrud
from database.models.payments import Payment

class PaymentManager(BasicCrud):

    def __init__(self):
        super().__init__(Payment)

    def payment_type_number(self,payment_type: str):
        payment = {
            'credit_card': 0,
            'boleto': 1,
            'pix': 2
        }
        return payment[payment_type]

    def payment_status(self,status: str):
        p = {
            'success': 0,
            'failed': 1,
            'cancelled': 2,
            'pending': 3
        }
        return p[status]

