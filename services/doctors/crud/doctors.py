from database.basic import BasicCrud
from database.models.doctors import Doctor

class DoctorManager(BasicCrud):

    def __init__(self):
        super().__init__(Doctor)