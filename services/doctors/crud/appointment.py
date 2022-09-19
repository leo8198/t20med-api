from datetime import datetime
import random
import string
from database.basic import BasicCrud
from database.models.appointments import Appointment

class AppointmentManager(BasicCrud):

    def __init__(self):
        super().__init__(Appointment)

    def generate_id(self):
        length = 8
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def get_status(self, status: str):
        p = {
            'scheduled': 0,
            'happening': 1,
            'done': 2,
            'cancelled': 3,
            'pending_payment': 4
        }
        return p[status]