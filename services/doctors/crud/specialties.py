from database.basic import BasicCrud
from database.models.specialties import DoctorSpecialty

class SpecialtiesManager(BasicCrud):

    def __init__(self):
        super().__init__(DoctorSpecialty)